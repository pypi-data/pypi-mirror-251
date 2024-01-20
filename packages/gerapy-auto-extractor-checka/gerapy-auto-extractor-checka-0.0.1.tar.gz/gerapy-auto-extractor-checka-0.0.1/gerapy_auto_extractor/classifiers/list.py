import joblib
import numpy as np
from glob import glob
from loguru import logger
from os.path import join, dirname, abspath
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from gerapy_auto_extractor.extractors.title import TitleExtractor
from gerapy_auto_extractor.patterns.datetime import METAS_MATCH as DATETIME_METAS
from gerapy_auto_extractor.schemas.element import Element
from gerapy_auto_extractor.utils.element import number_of_p_descendants, \
    number_of_a_descendants, number_of_punctuation, density_of_punctuation, density_of_text, number_of_clusters, \
    file2element, number_of_a_char, number_of_char, number_of_p_children
from gerapy_auto_extractor.utils.preprocess import preprocess4list_classifier
from gerapy_auto_extractor.utils.similarity import similarity1
from gerapy_auto_extractor.classifiers.base import BaseClassifier
import json

DATASETS_DIR = join(dirname(dirname(dirname(abspath(__file__)))), 'datasets')
MODELS_DIR = join(dirname(abspath(__file__)), 'models')


class ListClassifier(BaseClassifier):
    
    def __init__(self, models_path=None, dataset_dir=None):
        """
        init features and extractors
        :param model_path: classifier model file
        """
        self.models_path = models_path if models_path else MODELS_DIR
        self.model_path = join(self.models_path, 'list_model.pkl')
        self.scaler_path = join(self.models_path, 'list_scaler.pkl')
        self.dataset_dir = dataset_dir if dataset_dir else DATASETS_DIR
        self.title_extractor = TitleExtractor()
        self.feature_funcs = {     # ygh: 分别是什么含义？
            'number_of_a_char': number_of_a_char,
            'number_of_a_char_log10': self._number_of_a_char_log10,
            'number_of_char': number_of_char,
            'number_of_char_log10': self._number_of_char_log10,
            'rate_of_a_char': self._rate_of_a_char,
            'number_of_p_descendants': number_of_p_descendants,
            'number_of_a_descendants': number_of_a_descendants,
            'number_of_punctuation': number_of_punctuation,
            'density_of_punctuation': density_of_punctuation,
            'number_of_clusters': self._number_of_clusters,
            'density_of_text': density_of_text,
            'max_density_of_text': self._max_density_of_text,
            'max_number_of_p_children': self._max_number_of_p_children,
            'has_datetime_meta': self._has_datetime_mata,
            'similarity_of_title': self._similarity_of_title,
        }
        self.feature_names = self.feature_funcs.keys()
    
    def _number_of_clusters(self, element: Element):
        """
        get number of clusters like list
        :param element:
        :return:
        """
        tags = ['div', 'li', 'ul']
        return number_of_clusters(element, tags=tags)
    
    def _similarity_of_title(self, element: Element):
        """
        get similarity of <title> and (<h> or <meta>)
        :param element:
        :return:
        """
        _title_extract_by_title = self.title_extractor.extract_by_title(element)
        _title_extract_by_meta = self.title_extractor.extract_by_meta(element)
        _title_extract_by_h = self.title_extractor.extract_by_h(element)
        
        _title_target = None
        if _title_extract_by_meta:
            _title_target = _title_extract_by_meta
        elif _title_extract_by_h:
            _title_target = _title_extract_by_h
        
        if not _title_target:
            return 2
        if not _title_extract_by_title:
            return 3
        return similarity1(_title_target, _title_extract_by_title)
    
    def _has_datetime_mata(self, element: Element):
        """
        has datetime meta
        :param element:
        :return:
        """
        for xpath in DATETIME_METAS:
            datetime = element.xpath(xpath)
            if datetime:
                return True
        return False
    
    def _max_number_of_p_children(self, element: Element):
        """
        get max number of p children an element contains
        :param element:
        :return:
        """
        _number_of_p_children_list = []
        for descendant in element.descendants:
            _number_of_p_children = number_of_p_children(descendant)
            _number_of_p_children_list.append(_number_of_p_children)
        return max(_number_of_p_children_list)
    
    def _max_density_of_text(self, element: Element):
        """
        get max density_of_text
        :param element:
        :return:
        """
        _density_of_text_list = []
        for descendant in element.descendants:
            _density_of_text = density_of_text(descendant)
            _density_of_text_list.append(_density_of_text)
        return np.max(_density_of_text_list)
    
    def _rate_of_a_char(self, element: Element):
        """
        rate of a
        :param element:
        :return:
        """
        _number_of_a_char = number_of_a_char(element)
        _number_of_char = number_of_char(element)
        if _number_of_char == 0:
            return 0
        return _number_of_a_char / _number_of_char
    
    def _number_of_char_log10(self, element: Element):
        """
        log10 of number of char
        :param element:
        :return:
        """
        if element is None:
            return 0
        return np.log10(number_of_char(element) + 1)
    
    def _number_of_a_char_log10(self, element: Element):
        """
        log10 of number of a char
        :param element:
        :return:
        """
        if element is None:
            return 0
        return np.log10(number_of_a_char(element) + 1)
    
    def features_to_list(self, features: dict):
        """
        convert features to list
        :param features:
        :param label:
        :return:
        """
        return [features.get(feature_name) for feature_name in self.feature_names]
    
    def features(self, element: Element):
        """
        build feature map using element
        :param element:
        :return:
        """
        features = {}
        for feature_name, feature_func in self.feature_funcs.items():
            features[feature_name] = feature_func(element)
        return features
    
    def process(self, element: Element):
        """
        get probability of list
        :param element:
        :return:
        """
        preprocess4list_classifier(element)
        x = [self.features_to_list(self.features(element))]
        # scale
        ss = joblib.load(self.scaler_path)
        x = ss.transform(x)    # ?
        # load model
        clf = joblib.load(self.model_path)
        # predict
        result = clf.predict_proba(x)
        if result.any() and len(result) and len(result[0]):
            return result[0][1]
        return 0
    
    def train(self):
        """
        build dataset
        :return:
        """
        # 定义新的日志级别
        # logger.level("inspect", no=38, color="<yellow>")

        # 添加日志处理器以捕获 INSPECT 级别的日志
        logger.add("logfile.log", level="inspect")

        DATASETS_LIST_DIR = join(self.dataset_dir, 'list')
        DATASETS_DETAIL_DIR = join(self.dataset_dir, 'detail')
        list_file_paths = list(glob(f'{DATASETS_LIST_DIR}/*.html'))
        detail_file_paths = list(glob(f'{DATASETS_DETAIL_DIR}/*.html'))
        
        x_data, y_data = [], []
        
        for index, list_file_path in enumerate(list_file_paths):
            logger.log('inspect', f'list_file_path {list_file_path}')
            element = file2element(list_file_path)
            if element is None:
                continue
            preprocess4list_classifier(element)
            x = self.features_to_list(self.features(element))
            x_data.append(x)
            y_data.append(1)
        
        for index, detail_file_path in enumerate(detail_file_paths):
            logger.log('inspect', f'detail_file_path {detail_file_path}')
            element = file2element(detail_file_path)
            if element is None:
                continue
            preprocess4list_classifier(element)
            x = self.features_to_list(self.features(element))
            x_data.append(x)
            y_data.append(0)
        
        # preprocess data
        ss = StandardScaler()
        x_data = ss.fit_transform(x_data)
        joblib.dump(ss, self.scaler_path)
        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=5)
        
        # set up grid search
        c_range = np.logspace(-5, 20, 5, base=2)
        gamma_range = np.logspace(-9, 10, 5, base=2)
        param_grid = [
            {'kernel': ['rbf'], 'C': c_range, 'gamma': gamma_range},
            {'kernel': ['linear'], 'C': c_range},
        ]
        grid = GridSearchCV(SVC(probability=True), param_grid, cv=5, verbose=10, n_jobs=-1)
        clf = grid.fit(x_train, y_train)
        y_true, y_pred = y_test, clf.predict(x_test)
        logger.log('inspect', f'\n{classification_report(y_true, y_pred)}')
        score = grid.score(x_test, y_test)
        logger.log('inspect', f'test accuracy {score}')
        # save model
        joblib.dump(grid.best_estimator_, self.model_path)

    def train_new(self):
        """
        build dataset
        :return:
        """
        from .common import model_name, param_grid
        from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, StackingClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.svm import SVC
        from xgboost import XGBClassifier

        from sklearn.metrics import accuracy_score
        from sklearn.datasets import load_iris
        from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
        from sklearn.metrics import confusion_matrix, classification_report, cohen_kappa_score

        # 定义新的日志级别
        # logger.level("inspect", no=38, color="<yellow>")

        # 添加日志处理器以捕获 INSPECT 级别的日志
        logger.add("logfile.log", level="inspect")

        DATASETS_LIST_DIR = join(self.dataset_dir, 'list')
        DATASETS_DETAIL_DIR = join(self.dataset_dir, 'detail')
        list_file_paths = list(glob(f'{DATASETS_LIST_DIR}/*.html'))
        detail_file_paths = list(glob(f'{DATASETS_DETAIL_DIR}/*.html'))
        
        x_data, y_data = [], []
        
        for index, list_file_path in enumerate(list_file_paths):
            logger.log('inspect', f'list_file_path {list_file_path}')
            element = file2element(list_file_path)
            if element is None:
                continue
            preprocess4list_classifier(element)
            x = self.features_to_list(self.features(element))
            x_data.append(x)
            y_data.append(1)
        
        for index, detail_file_path in enumerate(detail_file_paths):
            logger.log('inspect', f'detail_file_path {detail_file_path}')
            element = file2element(detail_file_path)
            if element is None:
                continue
            preprocess4list_classifier(element)
            x = self.features_to_list(self.features(element))
            x_data.append(x)
            y_data.append(0)
        
        # preprocess data
        ss = StandardScaler()
        x_data = ss.fit_transform(x_data)
        joblib.dump(ss, self.scaler_path)
        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=5)

        model_object = {}
        model_object["rf"] = RandomForestClassifier()
        model_object["svm"] = SVC(probability=True)
        model_object["adaboost"] = AdaBoostClassifier()
        model_object["xgboost"] = XGBClassifier()

        grid_search = {}
        grid_search_random = {}
        best_params = {}
        best_params_random = {}
        best_estimator = {}
        for model in model_name:
            grid_search[model] = GridSearchCV(model_object[model], param_grid[model], cv=5, scoring='accuracy', n_jobs=-1)
            grid_search_random[model] = RandomizedSearchCV(model_object[model], param_grid[model], cv=5, scoring='accuracy', n_jobs=-1)
            grid_search[model].fit(x_train, y_train)
            grid_search_random[model].fit(x_train, y_train)
            best_params[model] = grid_search[model].best_params_
            best_params_random[model] = grid_search_random[model].best_params_
            best_estimator[model] = grid_search[model].best_estimator_
            file_path = join(self.models_path, 'classification_report_{}.txt'.format(model))
            with open(file_path, 'w') as file:
                file.write(model + "best_params:" + json.dumps(best_params[model]))
                file.write("\n\n")
                file.write(model + "best_params random:" + json.dumps(best_params_random[model]))
                file.write("\n\n")
            # print(model, "best_params:", best_params[model])
            # print(model, "best_params random:", best_params_random[model])
        
        pred_list = {}
        for model in model_name:
            pred = best_estimator[model].predict(x_test)
            pred_list[model] = pred

        overall_accuracies = {}
        for model in model_name:
            overall_accuracies[model] = accuracy_score(pred_list[model], y_test)
            print(model, "overall_accuracies:", overall_accuracies[model])
            cm = confusion_matrix(pred_list[model], y_test)
            report = classification_report(pred_list[model], y_test, digits=4)
            # cm, report = get_accuracy(pred_list[model], y_list, target_names=['Class 0', 'Class 1', "Class 2"])
            # print(cm, "\n\n", report)
            kappa = cohen_kappa_score(pred_list[model], y_test)
            file_path = join(self.models_path, 'classification_report_{}.txt'.format(model))
            with open(file_path, 'a') as file:
                for row in cm:
                    file.write(' '.join([str(elem) for elem in row]) + '\n')
                file.write(report)
                file.write("\n\n")
                file.write("kappa: " + str(kappa))
            if model in ["svm", "stacking"]:
                continue
            # print(model, best_estimator[model].feature_importances_)

        for model in model_name:
            tmp_path = join(self.models_path, 'list_model_{}.pkl'.format(model))
            joblib.dump(best_estimator[model], tmp_path)

        # # set up grid search
        # c_range = np.logspace(-5, 20, 5, base=2)
        # gamma_range = np.logspace(-9, 10, 5, base=2)
        # param_grid = [
        #     {'kernel': ['rbf'], 'C': c_range, 'gamma': gamma_range},
        #     {'kernel': ['linear'], 'C': c_range},
        # ]
        # grid = GridSearchCV(SVC(probability=True), param_grid, cv=5, verbose=10, n_jobs=-1)
        # clf = grid.fit(x_train, y_train)
        # y_true, y_pred = y_test, clf.predict(x_test)
        # logger.log('inspect', f'\n{classification_report(y_true, y_pred)}')
        # score = grid.score(x_test, y_test)
        # logger.log('inspect', f'test accuracy {score}')
        
        # save model
        # joblib.dump(grid.best_estimator_, self.model_path)

list_classifier = ListClassifier()


def probability_of_list(html, **kwargs):
    """
    get probability of list page
    :param html:
    :param kwargs: other kwargs
    :return:
    """
    return list_classifier.classify(html, **kwargs)

def probability_of_list_new(model: ListClassifier, html, **kwargs):
    """
    get probability of list page
    :param html:
    :param kwargs: other kwargs
    :return:
    """
    return model.classify(html, **kwargs)

def is_list(html, threshold=0.5, **kwargs):
    """
    judge if this page is list page
    :param html: source of html
    :param threshold:
    :param kwargs:
    :return:
    """
    _probability_of_list = probability_of_list(html, **kwargs)
    if _probability_of_list > threshold:
        return True
    return False

def is_list_new(model: ListClassifier, html, threshold=0.5, **kwargs):
    """
    judge if this page is list page
    :param html: source of html
    :param threshold:
    :param kwargs:
    :return:
    """
    _probability_of_list = probability_of_list_new(model, html, **kwargs)
    if _probability_of_list > threshold:
        return True
    return False