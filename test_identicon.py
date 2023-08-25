import identicon


def test_generate_image():
    john_image = identicon.generate_image("John")
    pixel1 = john_image.getpixel((0,0))
    pixel2 = john_image.getpixel((4,4))
    pixel3 = john_image.getpixel((4,7))
    assert pixel1 == (146, 242, 121)
    assert pixel2 == (131, 121, 242)
    assert pixel3 == (242, 166, 121)

def test_unique():
    """identical input strings create identical images, different ones do not"""
    john_image = identicon.generate_image("John")
    jon_image = identicon.generate_image("Jon")
    assert jon_image.tobytes() !=  john_image.tobytes()

    other_john_image = identicon.generate_image("John")
    assert other_john_image.tobytes() ==  john_image.tobytes()
