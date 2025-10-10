#!/usr/bin/env python3
"""Test image compression for particle format."""

import sys
sys.path.insert(0, 'src')

from image_processor import compress_pixel_row


def test_compress_pixel_row():
    """Test various compression scenarios."""

    # Test 1: Single 1's - should use uppercase letters
    assert compress_pixel_row('1') == 'A', "Single 1 should be 'A'"
    assert compress_pixel_row('11') == 'B', "Two 1's should be 'B'"
    assert compress_pixel_row('111') == 'C', "Three 1's should be 'C'"
    assert compress_pixel_row('1111') == 'D', "Four 1's should be 'D'"

    # Test 2: Trailing zeros should be dropped (including all zeros)
    assert compress_pixel_row('0') == '', "Single trailing 0 should be dropped"
    assert compress_pixel_row('00') == '', "Two trailing 0's should be dropped"
    assert compress_pixel_row('000') == '', "Three trailing 0's should be dropped"
    assert compress_pixel_row('0000') == '', "Four trailing 0's should be dropped"

    # Test 3: Trailing zeros should be dropped after content
    assert compress_pixel_row('1000') == 'A', "Trailing zeros should be dropped"
    assert compress_pixel_row('110') == 'B', "Trailing zeros should be dropped"
    assert compress_pixel_row('11110000') == 'D', "Trailing zeros should be dropped"

    # Test 4: Mixed patterns (non-trailing zeros are encoded)
    assert compress_pixel_row('101') == 'AaA', "1, 0, 1 should be 'AaA'"
    assert compress_pixel_row('011') == 'aB', "0 followed by two 1's should be 'aB'"
    assert compress_pixel_row('1100') == 'B', "Two 1's, two trailing 0's should be 'B'"
    assert compress_pixel_row('110011') == 'BbB', "Two 1's, two 0's, two 1's should be 'BbB'"

    # Test 5: Long runs (more than 26)
    assert compress_pixel_row('1' * 27) == 'ZA', "27 ones should be 'ZA' (26 + 1)"
    assert compress_pixel_row('1' * 52) == 'ZZ', "52 ones should be 'ZZ' (26 + 26)"
    assert compress_pixel_row('0' * 30 + '1') == 'zdA', "30 zeros and 1 one should be 'zdA' (26 + 4 + 1)"

    # Test 6: Complex pattern with trailing zeros
    assert compress_pixel_row('1110001100000') == 'CcB', "Complex pattern with trailing zeros"

    # Test 7: Alternating pattern
    assert compress_pixel_row('1010101') == 'AaAaAaA', "Alternating 1's and 0's ending with 1"

    print("All tests passed!")

    # Show some compression examples
    print("\nCompression examples:")
    examples = [
        '1111111111',
        '0000000000111111111100000',
        '1010101010',
        '111111111111111111111111111111',  # 30 ones
    ]

    for example in examples:
        compressed = compress_pixel_row(example)
        ratio = len(compressed) / len(example) if len(example) > 0 else 0
        print(f"  {example[:40]}{'...' if len(example) > 40 else ''}")
        print(f"  -> {compressed} (compression ratio: {ratio:.2%})")


if __name__ == '__main__':
    test_compress_pixel_row()
