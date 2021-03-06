# Annotation Guidelines
These are the guidelines for the annotation of olfactory references in historic artworks. 

## Basics
- We use [CVAT](https://github.com/openvinotoolkit/cvat) as image annotation tool. An instance is accessible via http://lme187.cs.fau.de:12444. 
- There is an extensive [manual](https://openvinotoolkit.github.io/cvat/docs/manual/) available at their github page.
- In order to create annotations, you need to be registered as a user. You can create one yourself or notify us, so we do it for you (preferred). 
- There is a slack channel `wp2-annotations` where we discuss annotation related issues. Please notify us if you would like to be added to the channel.

### Task Overview
- Once logged in, you will be taken to the task overview. The artworks are ordered thematically, depending on the query keywords that was used in image retrieval.
- Select one of the tasks according to your interest and the project need, by clicking on the `open` button. Our current annotation focus is `still-lifes-color`. 

![task overview](screenshots/task-overview.jpg)

### Job Overview
- Please mark that you are working on the job by entering your username in the `assignee` field on the right. 
- Each tasks consists of multiple jobs, each containing 50 artworks to be annotated. Select one job by clicking on the job name (e.g. `job #2842`) to start annotating. 
- Of course, it is possible (and encouraged) to review other users' jobs and share your thoughts on the slack channel or in the repository issues. 

![job overview](screenshots/job-overview.jpg)

### Annotation Window
- Having selected a job, you will see the first artwork that is waiting to be annotated. 
- You can navigate between artworks using the arrows on the top of the screen or by pushing the `f` and `n` buttons on the keyboard.
- Create your first box by clicking on the empty rectangle on the left (`1`) or by pushing the `n` button on the keyboard. 
- After creating the box, you can select a category for the box in the object tab on the right (`2`), by clicking on the `details` button (`3`) you can choose a subcategory. If no suitable subcategory is listed (and you think the subcategory is important as far as smell is concerned), you can enter a free text in the `other` field.
- For the annotations to be persisted, they must be saved using the `save` button in the top left corner, or by pushing `ctrl+s` on the keyboard. It is advisable to quicksave from time to time, so the annotations do not get lost if you accidentally close the browser.

![annotation window](screenshots/annotation-mode.png)

### Category Selection
- If there are many boxes of the same category to label, selecting a default label can speed up the process a lot.
- To do so, click on the `label` tab (`1`) on the right. 
- There you see all available high level categories. Some of them have numbers next to them (`2`).
- Push `ctrl + n` on the keyboard to select the category with number `n` next to it as default label for new bounding boxes, e.g. pushing `ctrl + 3` would select flower as the default label. 
- Since there are more than 10 possible categories, some of the categories do not have a number next to them but a `?` (`3`).
- To be able to select them as default category, a number has to be assigned first. To do so, simply click on the `?` (`3`), you can then select one number that should be replaced with the current category.

![label selection](screenshots/label-selection.png)

### Attribute Annotation
- In cases where many subcategories need to be selected, the attribute annotation mode can speed up the annotation. Select the attribute annotation mode by clicking on the dropdown menu in the top right corner of the screen (`1`).
- Now navigate through the attributes on the right until you see the `type` selection (`2`).

![attribute annotation prep](screenshots/attribute-annotation1.png)

- You can now conveniently select the appropriate subcategory by hitting the number key on the keyboard that is next the subcategory (`1`).
- Unfortunately, there is no shortcut for selecting subcategories with numbers higher than 10. In these cases, the type can be chosen by selecting it with the mouse in the list below.
- Navigate through the objects using the arrow buttons above (`2`) or by pushing `tab`/`shift+tab` on the keyboard.

![attribute annotation](screenshots/attribute-annotation2.png)


## Categories
- To limit the number of labels to choose from, the categories are ordered in a two level hierarchy where most categories contain a number of subcategories to further specify the annotation.
- A visualization of the hierarchy is available [here](labelsystem.jpg) 
- Apart from the predefined subcategories, each category has a generic `other` free text field where missing subcategories can be entered. 
- Furthermore, there is a specific `other` category that is meant to capture missing categories that the annotator thinks is important. It has a `type` free text field where the name of the missing category can be entered.
- Note that the annotation categories and their hierarchy do not match the way they are entered into the knowledge graph. There will be a separate mapping step before integrating the annotations there.
- If there is something you are absolutely missing from a nose-first perspective or you think is superfluous, please let us know, either in the issues, or in the slack channel.

## Best Practices

### Artwork Skipping 
- We are training the object detectors in an iterative process. In a first step, we want to train them using artworks that are as close as possible to photographic depictions. Then, in a second step, we will try to increase the level of artistic abstraction and expand our dataset to artworks that deviate more and more from photorealistic paintings. 
- This entails that grayscale images and images with a high level of abstraction should be skipped in the first round of annotations. Please just proceed to the next image if you encounter artworks where the objects are very hard to recognize (for you, as a human annotator).

### Subcategory Specification
- In the current stage of project we are not using the subcategories of many categories (e.g. flower or bird subcategories are not used). Other subcategories such as Mammal -> Dog are already used. 
- However, some of the subcategories may carry a lot of olfactory meaning (e.g. specific kinds of flowers), so be as specific as possible when defining the subcategory. 

### Instance Annotation
- In many artworks, objects are grouped together very closely with a lot of occlusion. Although it is hard to label each of these objects indidually, we currently do not have a way of handling crowd annotations. So, if possible, please try to label each instance separately. Zooming in and using the hotkeys `n` + default category can make this a little more convenient. 
- For cases where instance labeling is not possible, added the is_crowd attribute (based on the [coco iscrowd attribute](https://towardsdatascience.com/coco-data-format-for-object-detection-a4c5eaf518c5)) which can be checked in these cases. However, since we do not have a way of handling crowd references, try to avoid using this option.

## Hotkeys Cheatsheet
TBD

## Specific Category Guidelines

### Trees
- The tree category exists for historical reasons only, do not bother to annotate trees

### Beverages
- Beverages category is deprecated as well, please use "drinking vessel" where you can specify the contents if visible
- if the liquid content is not specifiable, use indefinable 
- cups should be annotated without plates
- different kind of "jugs" or in the subcategorie included. Maybe a better specification would be more convenient, especially for the last kind of "jug" 

![jug (1)](https://user-images.githubusercontent.com/91609811/165826544-61d33181-f834-44f6-b8b3-9b1348c06f46.png)![jug (2)](https://user-images.githubusercontent.com/91609811/165826565-63b89cc9-4cd2-4f34-9798-74d4f0b7c832.png)![jug (3)](https://user-images.githubusercontent.com/91609811/165826578-8a362e33-3f7c-4f23-99b2-e82211b1ee18.png)![jug (4)](https://user-images.githubusercontent.com/91609811/165826594-d805c122-581b-4d36-b04c-1bb3789bb76e.png)![jug (5)](https://user-images.githubusercontent.com/91609811/165826603-33610448-f300-4997-9e95-d3d19ca72b2c.png)

### Birds
- For now, we do not care about bird subtypes (we presume they smell alike), subtypes don't need to be specified

### Flower
- We define one instance of a flower as a visible blossom. Closed buds, leafs, and stems are not considered to be part of the flower instance.

### Fruit
- Grapes: One instance of an grapes-object is not a single berry, but the whole bunch of berries
- Lemon: Lemon (or in general citrus fruits) zests are included in the bounding box 
- only the fruit itself should be in the bounding box 

### Sniffing
- Please include the face (i.e. eyes, ears, nose) and the hand holding the object in the bounding box

### Whale
- In cases where a spout is visible, it is included in the bounding box
- If only the fluke is visible, whereas the rest of the body is under the water, the fluke is annotated, too.

### Gloves
- When overlapping, pairs of gloves are annotated as one instance, otherwise separately

### Jewellery
- Pomander: Only the pomander, not the chain holding it, is annotated

### Candle
- candlestand is included in the bounding box
- the burn of the candle is included in the bounding box 
- but make sure the fire on an candle is annotated as fire too

![candle and fire](https://user-images.githubusercontent.com/91609811/165826041-b25248cc-1ce9-48f3-a191-fb99879dbbdb.png)

### Censer
- Chains holding the censer are included in bounding box (if they are well visible)
- If there is smoke coming out of the censer, please keep in mind to annotate the smoke as well

### Smoking equipment 

- often there are broken pipes on the ground 

![broken pipe](https://user-images.githubusercontent.com/91609811/165825815-d5c0fce5-e807-4b6e-b87a-aafc35914f12.png)
- tobacco is often packed in addition to boxes also in paper

![tobacco box](https://user-images.githubusercontent.com/91609811/165825878-d0dfc1fb-1f8b-4386-aa9d-a949a187b7f9.png)  ![tabacco paper](https://user-images.githubusercontent.com/91609811/165825911-05476747-3533-4e35-a04d-874ff8492508.png)
- matches are mostly annotated as crowded 

![matches](https://user-images.githubusercontent.com/91609811/165825959-0ef59ebd-4356-4af8-a725-ecdffc6e0a30.png)
