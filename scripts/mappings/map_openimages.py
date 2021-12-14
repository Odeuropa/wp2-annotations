import pandas as pd
import cv2
import json
import argparse


def main():
    parser = argparse.ArgumentParser(description='Convert open images csv to coco json')
    parser.add_argument('--target', '-t', type=str, help='Where to store annotations')
    parser.add_argument('--source', '-s', type=str, help='Where to find oo annotations')
    parser.add_argument('--phase', '-p', type=str, choices=['train', 'eval'])
    args = parser.parse_args()

    TARGET_DIR = args.target
    PHASE = args.phase
    SOURCE = args.source

    oo_csv = pd.read_csv(f'/hdd/openimages/filtered_{PHASE}.csv')
    oo_im_dir = f'{SOURCE}/{PHASE}/data'
    with open ('/hdd/openimages/classmappings.json') as f:
        classmappings = json.load(f)


    print(oo_csv.columns)

    categories = {}
    images = {}
    annotations = {}
    oo_cat_to_coco_cat = {}
    image_ids_used = set()
    category_id_used = set()

    for index, ann in oo_csv.iterrows():
        labelName = ann['LabelName']
        if labelName not in classmappings:
            print(f'unused label {labelName}')
            continue
        if labelName not in category_id_used:
            id = len(categories) + 1
            oo_cat_to_coco_cat[labelName] = id
            categories[id] = {
                'id': id,
                'name': classmappings[labelName]
            }
            category_id_used.add(labelName)
        img_id = ann['ImageID']
        img = cv2.imread(f'{oo_im_dir}/{img_id}.jpg')
        h, w = img.shape[:2]
        if img_id not in image_ids_used:
            coco_img_id = len(image_ids_used)
            image_ids_used.add(img_id)
            img_entry = {
                'id': coco_img_id,
                'width': w,
                'height': h,
                'file_name': f'{img_id}.jpg'
            }
            images[img_id] = img_entry
        xMin = int(ann['XMin'] * w)
        yMin = int(ann['YMin'] * h)
        xMax = int(ann['XMax'] * w)
        yMax = int(ann['YMax'] * h)
        ann_entry = {
            'id': len(annotations) + 1,
            'image_id': coco_img_id,
            'category_id': oo_cat_to_coco_cat[labelName],
            'bbox': [
                xMin, yMin, xMax - xMin, yMax - yMin
            ],
            'area': (xMax - xMin) * (yMax - yMin),
            'iscrowd': 0
        }
        annotations[index+1] = ann_entry
        if (index % 500 == 0):
            print(f'{index}/{len(oo_csv)}')

    coco_json = {
        'images': list(images.values()),
        'annotations': list(annotations.values()),
        'categories': list(categories.values())
    }

    with open(f'{TARGET_DIR}/instances_{PHASE}.json', 'w') as outfile:
        json.dump(coco_json, outfile)


    print(len(images))


if __name__ == '__main__':
    main()