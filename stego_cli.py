import os
import argparse
from anyedgestego import EdgeStego


def validate_input_path(input_path):
    if not os.path.exists(input_path) or not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file {input_path} does not exist or is not a file.")


def validate_output_dir(output_dir):
    if not os.path.exists(output_dir) or not os.path.isdir(output_dir):
        raise NotADirectoryError(f"Output directory {output_dir} does not exist or is not a directory.")


def encode(input_path, text, output_dir):
    # Validate the input path and output directory
    validate_input_path(input_path)
    # validate_output_dir(output_dir)

    # Create an EdgeStego instance for encoding
    stego = EdgeStego(operation='encode', input_filename=input_path, input_text=text, output_filename=output_dir)

    # Perform the encoding
    stego.encode_image()

    # Display the number of bits taken to encode
    print(f"Number of bits taken to encode: {stego.hiddenTextBitLength}")

    # Display the path to the encoded image
    print(f"Encoded image saved to {output_dir}")


def decode(input_path, bits):
    # Validate the input path
    validate_input_path(input_path)

    # Create an EdgeStego instance for decoding
    stego = EdgeStego(operation='decode', input_filename=input_path, bits_to_decode=bits)

    # Perform the decoding
    decoded_text = stego.decode_image()

    # Display the decoded text
    print(f"Decoded Text: {decoded_text}")


def inspect(input_path):
    # Validate the input path
    validate_input_path(input_path)

    stego = EdgeStego(operation='inspect', input_filename=input_path)

    print(f"Number of bits that can be encoded: {stego.inspect_image()}")


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="EdgeStego CLI")

    # Define subparsers for encode and decode operations
    subparsers = parser.add_subparsers(dest='operation', required=True)

    # Define the encode subparser
    parser_encode = subparsers.add_parser('encode', help='Encode text into an image')
    parser_encode.add_argument('-i', '--input', required=True, help='Path to the input image')
    parser_encode.add_argument('-t', '--text', required=True, help='Text to encode')
    parser_encode.add_argument('-o', '--output', required=True, help='Directory to save the encoded image')

    # Define the decode subparser
    parser_decode = subparsers.add_parser('decode', help='Decode text from an image')
    parser_decode.add_argument('-i', '--input', required=True, help='Path to the image to decode')
    parser_decode.add_argument('-b', '--bits', required=True, type=int, help='Number of bits to decode')

    # Define the inspect subparser
    parser_inspect = subparsers.add_parser('inspect',
                                           help='Inspect an image, return the number of possible characters that can '
                                                'be encoded')
    parser_inspect.add_argument('-i', '--input', required=True, help='Path to the image to inspect')

    args = parser.parse_args()

    if args.operation == 'encode':
        # Encode the text into an image
        encode(args.input, args.text, args.output)
    elif args.operation == 'decode':
        # Decode the text from an image
        decode(args.input, args.bits)
    elif args.operation == 'inspect':
        # Inspect the image
        inspect(args.input)
    else:
        print("Invalid operation. Use 'encode' to encode text into an image or 'decode' to decode text from an image.")


if __name__ == "__main__":
    main()
