import sys
import os

# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上层目录
parent_dir = os.path.dirname(current_dir)
# 将上层目录添加到sys.path
sys.path.append(parent_dir)

import unittest
from tests.test_base import TestBase
from gerapy_auto_extractor.classifiers.list import is_list, is_list_new, ListClassifier
from gerapy_auto_extractor.classifiers.detail import is_detail, is_detail_new

import os

model_path_base = "/mnt/e/codes/llm-checka/page_classifier/GerapyAutoExtractor/gerapy_auto_extractor/classifiers/models"
# model_path_base = "/mnt/e/codes/llm-checka/page_classifier/GerapyAutoExtractor/gerapy_auto_extractor/classifiers/models/new"
# model_path_base = "/mnt/e/codes/llm-checka/page_classifier/GerapyAutoExtractor/gerapy_auto_extractor/classifiers/models/new_4_classifiers"
if not os.path.exists(model_path_base):
    os.makedirs(model_path_base)
dataset_path_base = "/mnt/e/data/checka/page-classification/html-files"
dataset_path_base = "/mnt/e/data/checka/page-classification/html-files2"

list_classifier = ListClassifier(models_path=model_path_base, dataset_dir=dataset_path_base)


class TestAccuracy(TestBase):

    def compute_accuracy(self, folder_path):
        """
        计算is_list和is_detail函数的精度。

        Args:
            folder_path (str): 包含两个子文件夹（list和detail）的主文件夹路径。

        Returns:
            dict: 包含is_list精度和is_detail精度的字典。
        """
        correct_all = 0
        correct_list_predictions = 0
        correct_detail_predictions = 0
        total_all = 0
        total_list_samples = 0
        total_detail_samples = 0

        # 处理列表文件夹
        list_dir = os.path.join(folder_path, 'list')
        list_err_dir = os.path.join(folder_path, 'list_err')
        if not os.path.exists(list_err_dir):
            os.makedirs(list_err_dir)
        for file_name in os.listdir(list_dir):
            print("list", file_name)
            file_path = os.path.join(list_dir, file_name)
            html = self.content(file_path)
            # if is_list(html):
            if is_list_new(list_classifier, html):
                correct_list_predictions += 1
            else:
                print("list error", file_name)
                # copy error file to list_err folder
                os.system(f"cp {file_path} {list_err_dir}")
            total_list_samples += 1

        # 处理详情页文件夹
        detail_dir = os.path.join(folder_path, 'detail')
        detail_err_dir = os.path.join(folder_path, 'detail_err')
        if not os.path.exists(detail_err_dir):
            os.makedirs(detail_err_dir)
        for file_name in os.listdir(detail_dir):
            print("detail", file_name)
            file_path = os.path.join(detail_dir, file_name)
            html = self.content(file_path)
            # if is_detail(html):
            if is_detail_new(list_classifier, html):
                correct_detail_predictions += 1
            else:
                print("detail error", file_name)
                # copy error file to detail_err folder
                os.system(f"cp {file_path} {detail_err_dir}")
            total_detail_samples += 1

        # 计算精度
        list_accuracy = correct_list_predictions / total_list_samples
        detail_accuracy = correct_detail_predictions / total_detail_samples

        total_all = total_list_samples + total_detail_samples
        correct_all = correct_list_predictions + correct_detail_predictions
        total_accuracy = correct_all / total_all

        return {
            'total_accuracy': total_accuracy,
            'list_accuracy': list_accuracy,
            'detail_accuracy': detail_accuracy
        }

# 示例使用
if __name__ == '__main__':
    test = TestAccuracy()
    # folder_path = "/mnt/e/codes/llm-checka/page_classifier/GerapyAutoExtractor/samples"
    folder_path = "/mnt/e/data/checka/page-classification/html-files"
    folder_path = "/mnt/e/data/checka/page-classification/html-files2"
    accuracies = test.compute_accuracy(folder_path)
    print(f"is_list精度: {accuracies['list_accuracy']:.2f}")
    print(f"is_detail精度: {accuracies['detail_accuracy']:.2f}")
    print(f"总精度: {accuracies['total_accuracy']:.2f}")
