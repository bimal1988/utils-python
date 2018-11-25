from glob import glob
import os
import re
import xml.etree.ElementTree as ET


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split('(\d+)', text)]


def create_train_test_files(src):
    imgs = glob('{}/*.jpg'.format(src))
    imgs.sort(key=natural_keys)

    with open('train.txt', 'wt') as train:
        with open('test.txt', 'wt') as test:
            i = 1
            for imgname in imgs:
                if i % 5 == 0:
                    test.write('data/{}\n'.format(imgname))
                else:
                    train.write('data/{}\n'.format(imgname))
                i += 1


def convert_voc_to_yolo(voc_anno_dir, yolo_obj_path):
    anno_xlms = glob('{}/*.xml'.format(voc_anno_dir))
    name_dict = {'Flame': '0', 'Smoke': '1', 'Steam': '2'}
    for xml in anno_xlms:
        fname = os.path.splitext(
            yolo_obj_path + '/' + os.path.basename(xml))[0] + '.txt'
        with open(fname, 'wt') as f:
            tree = ET.parse(xml)
            root = tree.getroot()
            img_width = float(root.find('./size/width').text)
            img_height = float(root.find('./size/height').text)
            newline = ''
            for obj in root.findall('object'):
                anno_name = obj.find('name').text
                anno_xmin = float(obj.find('bndbox/xmin').text)
                anno_ymin = float(obj.find('bndbox/ymin').text)
                anno_xmax = float(obj.find('bndbox/xmax').text)
                anno_ymax = float(obj.find('bndbox/ymax').text)

                center_x = (anno_xmax + anno_xmin) / (2 * img_width)
                center_y = (anno_ymax + anno_ymin) / (2 * img_height)
                anno_width = (anno_xmax - anno_xmin) / img_width
                anno_height = (anno_ymax - anno_ymin) / img_height

                yolo_str = newline + name_dict[anno_name]
                yolo_str += ' {}'.format(round(center_x, 6))
                yolo_str += ' {}'.format(round(center_y, 6))
                yolo_str += ' {}'.format(round(anno_width, 6))
                yolo_str += ' {}'.format(round(anno_height, 6))

                newline = '\n'

                f.write(yolo_str)


if __name__ == '__main__':
    # Change current working directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    convert_voc_to_yolo(
        '/Users/bimal/Desktop/FlareWatchDataSet/170413-082313/pascal-voc/Annotations', 'obj')
