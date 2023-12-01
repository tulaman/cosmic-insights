from utils import get_horoscope

# test the external API from Horoscope Astrology
def test_gethoroscope():
    horoscope = get_horoscope('today', 'aries')
    assert len(horoscope['horoscope']) > 0

# the same test for virgo
def test_gethoroscope2():
    horoscope = get_horoscope('today', 'virgo')
    assert len(horoscope['horoscope']) > 0