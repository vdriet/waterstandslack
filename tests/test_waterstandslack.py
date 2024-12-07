from unittest import TestCase
from unittest.mock import patch


class Test(TestCase):
  @patch('waterstandslack.checkwaterstandenpost')
  def test_main(self, mock_checkwaterstandenpost):
    import waterstandslack

    waterstandslack.main()
    assert mock_checkwaterstandenpost.called
