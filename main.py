from PIL import Image
import random

def get_image_width(image_name):
    with open(image_name + '.txt', 'r') as file:
        line = file.readline()
        pixel_count = len(line) // 24
        return pixel_count

def get_image_height(image_name):
    with open(image_name + '.txt', 'r') as file:
        lines = file.readlines()
        return len(lines)

def get_image_pixels(image_name):
    width = get_image_width(image_name)
    height = get_image_height(image_name)
    pixel_count = width * height
    return pixel_count

def image_to_text(image_name):
    with Image.open(image_name + '.png') as image:
        image = image.convert('RGB')
        width, height = image.size
        with open(image_name + '.txt', 'w') as file:
            for y in range(height):
                for x in range(width):
                    r, g, b = image.getpixel((x, y))
                    file.write(f"{format(r, '08b')}{format(g, '08b')}{format(b, '08b')}")
                file.write('\n')

def text_to_image(image_name):
    width = get_image_width(image_name)
    height = get_image_height(image_name)
    image = Image.new('RGB', (width, height))
    with open(image_name + '.txt', 'r') as file:
        pixels = []
        for line in file:
            line = line.replace('\n', '')
            for i in range(0, len(line), 24):
                r = int(line[i : i + 8], 2)
                g = int(line[i + 8 : i + 16], 2)
                b = int(line[i + 16 : i + 24], 2)
                pixels.append((r, g, b))
    image.putdata(pixels)
    image.save(image_name + '.png')

def add_error_to_image(source_image_name, destination_image_name, error_rate):
    with open(source_image_name + '.txt', 'r') as source_file:
        source_content = source_file.read()
    modified_content = []
    for char in source_content:
        if char in '01' and random.random() < error_rate:
            modified_content.append('1' if char == '0' else '0')
        else:
            modified_content.append(char)
    with open(destination_image_name + '.txt', 'w') as destination_file:
        destination_file.write(''.join(modified_content))

def count_different_pixels(first_image_name, second_image_name):
    with open(first_image_name + '.txt', 'r') as first_file, open(second_image_name + '.txt', 'r') as second_file:
        first_content = first_file.read().replace('\n', '')
        second_content = second_file.read().replace('\n', '')
    different_pixels = 0
    for i in range(len(first_content) // 24):
        start = i * 24
        end = start + 24
        if first_content[start : end] != second_content[start : end]:
            different_pixels += 1
    return different_pixels

SYMBOL = 8
CODEWORD = 255 * SYMBOL
MESSAGE = 239 * SYMBOL
CAPABILITY = (CODEWORD - MESSAGE) // SYMBOL // 2

def count_different_bits(first_image_name, second_image_name):
    with open(first_image_name + '.txt', 'r') as first_file, open(second_image_name + '.txt', 'r') as second_file:
        first_content = first_file.read().replace('\n', '')
        second_content = second_file.read().replace('\n', '')
    difference_count = sum(first_bit != second_bit for first_bit, second_bit in zip(first_content, second_content))
    return difference_count

def count_different_symbols(first_image_name, second_image_name):
    with open(first_image_name + '.txt', 'r') as first_file, open(second_image_name + '.txt', 'r') as second_file:
        first_content = first_file.read().replace('\n', '')
        second_content = second_file.read().replace('\n', '')
    different_symbols = 0
    for i in range(len(first_content) // SYMBOL):
        start = i * SYMBOL
        end = start + SYMBOL
        if first_content[start : end] != second_content[start : end]:
            different_symbols += 1
    return different_symbols

def count_different_messages(first_image_name, second_image_name):
    with open(first_image_name + '.txt', 'r') as first_file, open(second_image_name + '.txt', 'r') as second_file:
        first_content = first_file.read().replace('\n', '')
        second_content = second_file.read().replace('\n', '')
    different_messages = 0
    for i in range(len(first_content) // MESSAGE):
        start = i * MESSAGE
        end = start + MESSAGE
        if first_content[start : end] != second_content[start : end]:
            different_messages += 1
    return different_messages

def correct_error_to_image(original_image_name, error_added_image_name, destination_image_name):
    with open(original_image_name + '.txt', 'r') as original_file, open(error_added_image_name + '.txt', 'r') as error_added_file:
        original_content = original_file.read().replace('\n', '')
        error_added_content = error_added_file.read().replace('\n', '')
    destination_content = []
    for i in range(len(original_content) // MESSAGE + 1):
        message_start = i * MESSAGE
        message_end = len(original_content) if i == len(original_content) // MESSAGE else message_start + MESSAGE
        different_symbols = 0
        for j in range((message_end - message_start) // SYMBOL):
            symbol_start = message_start + j * SYMBOL
            symbol_end = symbol_start + SYMBOL
            if original_content[symbol_start : symbol_end] != error_added_content[symbol_start : symbol_end]:
                different_symbols += 1
        if different_symbols > CAPABILITY:
            destination_content.append(error_added_content[message_start : message_end])
        else:
            destination_content.append(original_content[message_start : message_end])
    destination_content = ''.join(destination_content)
    width = get_image_width(original_image_name)
    height = get_image_height(original_image_name)
    destination_index = 0
    with open(destination_image_name + '.txt', 'w') as destination_file:
        for _ in range(height):
            destination_file.write(destination_content[destination_index : destination_index + width * 24])
            destination_index += width * 24
            destination_file.write('\n')

ERROR_RATE = 0.001
ITERATIONS = 10

image_0 = 'image_0'
image_to_text(image_0)
image_0_bits = get_image_pixels(image_0) * 24
image_0_symbols = image_0_bits // SYMBOL
image_0_messages = image_0_bits // MESSAGE
image_0_pixels = get_image_pixels(image_0)
print('\t\t\t\tQuantity\t\tRatio')

pre_fec_ber_file = open('output_pre_fec_ber.txt', 'w')
pre_fec_ser_file = open('output_pre_fec_ser.txt', 'w')
pre_fec_bler_file = open('output_pre_fec_bler.txt', 'w')
post_fec_ber_file = open('output_post_fec_ber.txt', 'w')
post_fec_ser_file = open('output_post_fec_ser.txt', 'w')
post_fec_bler_file = open('output_post_fec_bler.txt', 'w')
for i in range(ITERATIONS):
    print(f"Performing {i}{'th' if 10 <= i % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(i % 10, 'th')} iteration ...")
    
    image_1 = 'image_1'
    add_error_to_image(image_0, image_1, ERROR_RATE)
    text_to_image(image_1)
    image_1_different_pixels = count_different_pixels(image_0, image_1)
    image_1_different_pixels_ratio = image_1_different_pixels / image_0_pixels
    image_1_different_bits = count_different_bits(image_0, image_1)
    image_1_different_bits_ratio = image_1_different_bits / image_0_bits
    image_1_different_symbols = count_different_symbols(image_0, image_1)
    image_1_different_symbols_ratio = image_1_different_symbols / image_0_symbols
    image_1_different_messages = count_different_messages(image_0, image_1)
    image_1_different_messages_ratio = image_1_different_messages / image_0_messages
    print(f"Different pixels in {image_1}:\t{image_1_different_pixels :016d}\t{image_1_different_pixels_ratio :.16f}")
    print(f"Different bits in {image_1}:\t{image_1_different_bits :016d}\t{image_1_different_bits_ratio :.16f}")
    print(f"Different symbols in {image_1}:\t{image_1_different_symbols :016d}\t{image_1_different_symbols_ratio :.16f}")
    print(f"Different messages in {image_1}:\t{image_1_different_messages :016d}\t{image_1_different_messages_ratio :.16f}")

    image_2 = 'image_2'
    correct_error_to_image(image_0, image_1, image_2)
    text_to_image(image_2)
    image_2_different_pixels = count_different_pixels(image_0, image_2)
    image_2_different_pixels_ratio = image_2_different_pixels / image_0_pixels
    image_2_different_bits = count_different_bits(image_0, image_2)
    image_2_different_bits_ratio = image_2_different_bits / image_0_bits
    image_2_different_symbols = count_different_symbols(image_0, image_2)
    image_2_different_symbols_ratio = image_2_different_symbols / image_0_symbols
    image_2_different_messages = count_different_messages(image_0, image_2)
    image_2_different_messages_ratio = image_2_different_messages / image_0_messages
    print(f"Different pixels in {image_2}:\t{image_2_different_pixels :016d}\t{image_2_different_pixels_ratio :.16f}")
    print(f"Different bits in {image_2}:\t{image_2_different_bits :016d}\t{image_2_different_bits_ratio :.16f}")
    print(f"Different symbols in {image_2}:\t{image_2_different_symbols :016d}\t{image_2_different_symbols_ratio :.16f}")
    print(f"Different messages in {image_2}:\t{image_2_different_messages :016d}\t{image_2_different_messages_ratio :.16f}")

    pre_fec_ber_file.write(f"{image_1_different_bits_ratio :.16f}\n")
    pre_fec_ser_file.write(f"{image_1_different_symbols_ratio :.16f}\n")
    pre_fec_bler_file.write(f"{image_1_different_messages_ratio :.16f}\n")
    post_fec_ber_file.write(f"{image_2_different_bits_ratio :.16f}\n")
    post_fec_ser_file.write(f"{image_2_different_symbols_ratio :.16f}\n")
    post_fec_bler_file.write(f"{image_2_different_messages_ratio :.16f}\n")
    print('')
pre_fec_ber_file.close()
pre_fec_ser_file.close()
pre_fec_bler_file.close()
post_fec_ber_file.close()
post_fec_ser_file.close()
post_fec_bler_file.close()

def average_calculation(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        numbers = [float(line.strip()) for line in lines]
        if numbers:
            average = sum(numbers) / len(numbers)
        return average

print(f"Pre FEC BER:\t{average_calculation('output_pre_fec_ber.txt') :.16f}")
print(f"Pre FEC SER:\t{average_calculation('output_pre_fec_ser.txt') :.16f}")
print(f"Pre FEC BLER:\t{average_calculation('output_pre_fec_bler.txt') :.16f}")
print(f"Post FEC BLER:\t{average_calculation('output_post_fec_bler.txt') :.16f}")
print(f"Post FEC SER:\t{average_calculation('output_post_fec_ser.txt') :.16f}")
print(f"Post FEC BER:\t{average_calculation('output_post_fec_ber.txt') :.16f}")
