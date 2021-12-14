import pandas as pd
import argparse
import cv2
import json
from tqdm import tqdm


def coco_from_df(df, img_dir, catmap, categories):
        print(f'Creating coco json for {len(df)} annotations.')
        img_ids = set()
        annotations = []
        images = []
        for ann in tqdm(df.iterrows()):
                ann = ann[1]
                img_id = ann['ImageID']
                if img_id not in img_ids:
                        img = cv2.imread(f'{img_dir}/{img_id}.jpg')
                        if img is None:
                                print('broken')
                                # ignore broken images
                                continue
                        h, w = img.shape[:2]
                        img_entry = {
                                'id': len(img_ids) + 1,
                                'width': w,
                                'height': h,
                                'file_name': f'{img_id}.jpg'
                        }
                        images.append(img_entry)
                        img_ids.add(img_id)
                xMin = int(ann['XMin'] * w)
                yMin = int(ann['YMin'] * h)
                xMax = int(ann['XMax'] * w)
                yMax = int(ann['YMax'] * h)
                annotation = {
                        'id': len(annotations) + 1,
                        'image_id': img_id,
                        'category_id': catmap[ann['LabelName']],
                        'bbox': [xMin, yMin, xMax - xMin, yMax - yMin],
                        'area': (xMax - xMin) * (yMax - yMin),
                        'iscrowd': 0
                }
                annotations.append(annotation)

        print('Coco json created successfully.')
        return {
                'images': images,
                'annotations': annotations,
                'categories': categories
        }

def main():
        parser = argparse.ArgumentParser(description='Filter open images csv for list of classes')
        parser.add_argument('--phase', '-p', type=str, choices=['train','eval'], default='train')
        parser.add_argument('--filter_cats', type=str, default='supercats_oi.json', help='path to json with categories that should be used.')
        parser.add_argument('--mapping_file', '-f', default='oi_to_supercats.json')
        parser.add_argument('--imgdir', '-i')
        args = parser.parse_args()

        PHASE = args.phase

        category_mappings = pd.read_csv(f'/hdd/open-images-v6/{PHASE}/metadata/classes.csv', header=None, names=['id','name'], index_col='name')

        nameToId = category_mappings.to_dict()['id']
        idToName = {v:k for k,v in nameToId.items()}

        with open(args.filter_cats) as f:
                filter_cats = json.load(f)

        filter_ids = [nameToId[name] for name in filter_cats]

        labels_df = pd.read_csv(f'/hdd/open-images-v6/{PHASE}/labels/detections.csv')

        labels_filtered = labels_df[labels_df["LabelName"].isin(filter_ids)]

        label_count = labels_filtered['LabelName'].value_counts()
        name_count = {idToName[k]: v for k,v in label_count.to_dict().items()}
        print(name_count)


        labels_filtered = labels_df[labels_df["LabelName"].isin(filter_ids)]
        labels_new = labels_filtered[labels_filtered['LabelName']== 'None']

        with open(args.mapping_file) as f:
                mapping_json = json.load(f)

        oi_coco = coco_from_df(labels_filtered, args.imgdir, mapping_json['mappings'], mapping_json['categories'])

        for ann in labels_filtered.iterrows():
                cat_id = ann[1]['LabelName']
                labels_new = labels_new.append(ann[1])


        labels_new.to_csv(f'/hdd/openimages/catscut/filtered_{PHASE}.csv')

        print('done')


if __name__ == '__main__':
        main()