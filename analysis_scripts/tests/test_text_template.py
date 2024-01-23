import unittest
from analytics import text_template

class TestTextTemplate(unittest.TestCase):

    def test_text_template_us(self):
        expected = """
## Inpatient US

Inpatient imaging under 24h

![]({{'/assets/images/IPUS_imaging_24h.png' | relative_url}})

Inpatient reporting under 4h

![]({{'/assets/images/IPUS_reporting_4h.png' | relative_url}})
"""
        self.assertEqual(text_template('US'), expected)
