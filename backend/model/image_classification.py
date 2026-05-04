import cv2
import numpy as np

# Read classes
with open('./data/classification_classes_ILSVRC2012.txt', 'r') as f:
        names_set = f.read().split('\n')

class_names = [name.split(',')[0] for name in names_set]

# Load model
model = cv2.dnn.readNet('./data/DenseNet_121.caffemodel', './data/DenseNet_121.prototxt', framework='Caffe')

# Prepare image
image = cv2.imread('./data/image.png')
blob = cv2.dnn.blobFromImage(image=image, scalefactor=0.01, size=(224, 224), mean=(104, 117, 123))

# Pass image to model
model.setInput(blob)
outputs = model.forward()

# Prepare output
final_outputs = outputs[0]
final_outputs = final_outputs.reshape(1000, 1)
label_id = np.argmax(final_outputs)
probs = np.exp(final_outputs) / np.sum(np.exp(final_outputs))
final_prob = np.max(probs) * 100.
out_name = class_names[label_id]
print(out_name)