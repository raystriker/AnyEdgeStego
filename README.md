
# AnyEdgeStego

AnyEdgeStego is a steganography tool allowing users to hide text within the edges of an image, providing functionalities to encode text into an image, decode hidden text from an image, and inspect an image to determine how much potential text it can conceal.

## Installation

To install AnyEdgeStego, clone the repository and install the necessary requirements:

```sh
git clone https://github.com/raystriker/AnyEdgeStego.git
cd anyedgestego
pip install -r requirements.txt
```

## Usage

### 1. Encoding Text into an Image

To encode text into an image, use the `encode` operation, specifying the input image path, the text to encode, and the output directory to save the modified image:

```sh
python stego_cli.py encode --input /path/to/image --text "Secret Text" --output /path/to/output_dir
```

### 2. Decoding Text from an Image

To decode the hidden text from an image, use the `decode` operation, specifying the input image path and the number of bits to decode:

```sh
python stego_cli.py decode --input /path/to/image --bits NUMBER_OF_BITS
```

### 3. Inspecting an Image

To inspect an image and determine the number of bits that can be encoded, use the `inspect` operation, specifying the input image path:

```sh
python stego_cli.py inspect --input /path/to/image
```

## Limitations

##### 1. The output (encoded) file must be a BMP file format or bitmap file
##### 2. Only a certain amount of bits can be encoded, it's recommended to "inspect" the input image first


## Examples

Here are some example usages of the AnyEdgeStego tool:

```sh
# Encoding example
python stego_cli.py encode --input example.jpg --text "Hello, World!" --output encoded_image.bmp

# Decoding example
python stego_cli.py decode --input encoded_image.bmp --bits 12

# Inspecting example
python stego_cli.py inspect --input example.bmp
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

