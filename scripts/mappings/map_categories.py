""" Script to map annotation categories to experiment labels
Maps categories from labels file (-l) to target labels (-t) using mapping file (-m).
Mapped annotations are written into labels file dir.
"""
import json
import argparse
import os


def map_annotations(cvat_json, mapping_json):
    direct_mappings = mapping_json['direct_mappings']
    type_mappings = mapping_json['type_mappings']

    mapped_annotations = []
    for ann in cvat_json['annotations']:
        cat_id = str(ann['category_id'])
        if cat_id in direct_mappings.keys():
            ann['category_id'] = direct_mappings[cat_id]
            mapped_annotations.append(ann)
        elif 'type' in ann['attributes']:
            subtype = ann['attributes']['type']
            if subtype in type_mappings.keys():
                ann['category_id'] = type_mappings[subtype]
                mapped_annotations.append(ann)

    used_img_ids = {ann['image_id'] for ann in mapped_annotations}
    used_imgs = [img for img in cvat_json['images'] if img['id'] in used_img_ids]

    mapped_json = {
        'images': used_imgs,
        'annotations': mapped_annotations,
        'categories': mapping_json['categories']
    }

    return mapped_json

def helper(cvat_json, mapping_json):
    names = set([cat['name'] for cat in cvat_json['categories']])

    name_to_id_mapping = {cat['name'].lower(): cat['id'] for cat in mapping_json['categories']}

    unused_names = []
    name_mappings = {}
    for name in names:
        try:
            new_id = name_to_id_mapping[name]
            name_mappings[name] = new_id
        except KeyError:
            unused_names.append(name)

    print(unused_names)

    return None


def map_with_names(source_coco, mapping_json):
    name_mappings = mapping_json['name_mappings']

    cat_id_to_name = {cat['id']: cat['name'] for cat in source_coco['categories']}
    mapped_annotations = []
    skipped = []
    for ann in source_coco['annotations']:
        cat_name = cat_id_to_name[ann['category_id']]

        try:
            new_cat_id = name_mappings[cat_name]
            ann['category_id'] = new_cat_id
            mapped_annotations.append(ann)
        except KeyError:
            skipped.append(cat_name)


    used_img_ids = {ann['image_id'] for ann in mapped_annotations}
    used_imgs = [img for img in source_coco['images'] if img['id'] in used_img_ids]

    mapped_json = {
        'images': used_imgs,
        'annotations': mapped_annotations,
        'categories': mapping_json['categories']
    }

    return mapped_json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mapping_file', '-m', help='path to mapping json file')
    parser.add_argument('--labels', '-l', help='path to cvat labels in coco format')
    args = parser.parse_args()
    with open(args.labels) as f:
        source_coco = json.load(f)
    with open(args.mapping_file) as f:
        mapping_json = json.load(f)

    # mapped_coco = map_annotations(source_coco, mapping_json)
    mapped_coco = map_with_names(source_coco, mapping_json)

    write_dir = os.path.dirname(args.labels)
    # target_path = f'{write_dir}/instances_mapped.json'
    target_path = f'{write_dir}/instances_mapped_icpr.json'
    with open(target_path, 'w') as f:
        json.dump(mapped_coco, f)

    print(f'Mapped annotations written to: {target_path}.')


if __name__ == "__main__":
    main()
