import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, add
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle

# Load the pre-trained ResNet50 model for feature extraction
resnet_model = ResNet50(weights='imagenet')
feature_extractor = Model(inputs=resnet_model.input, outputs=resnet_model.layers[-2].output)

# Function to extract features from an image
def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = feature_extractor.predict(img_array)
    return features

# Define the caption generation model
def define_caption_model(vocab_size, max_length):
    inputs1 = Input(shape=(2048,))
    fe1 = Dense(256, activation='relu')(inputs1)
    fe2 = tf.expand_dims(fe1, 1)

    inputs2 = Input(shape=(max_length,))
    se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = LSTM(256)(se1)

    decoder1 = add([fe2, se2])
    decoder2 = LSTM(256)(decoder1)
    outputs = Dense(vocab_size, activation='softmax')(decoder2)

    model = Model(inputs=[inputs1, inputs2], outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model

# Load the tokenizer and pre-trained model weights
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

vocab_size = len(tokenizer.word_index) + 1
max_length = 30  # Adjust based on your data
caption_model = define_caption_model(vocab_size, max_length)
caption_model.load_weights('caption_model_weights.h5')

# Function to generate a caption for an image
def generate_caption(model, tokenizer, photo, max_length):
    in_text = 'startseq'
    for _ in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = tokenizer.index_word.get(yhat)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'endseq':
            break
    final_caption = in_text.split(' ')[1:-1]
    return ' '.join(final_caption)

# Example usage
def main():
    img_path = 'example_image.jpg'
    photo = extract_features(img_path)
    caption = generate_caption(caption_model, tokenizer, photo, max_length)
    print("Caption:", caption)

if __name__ == "__main__":
    main()
