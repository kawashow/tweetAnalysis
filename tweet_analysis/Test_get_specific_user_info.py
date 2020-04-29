import unittest
from tweet_analysis.get_specific_user_info import GetSpecificUserInfo


class TestGetSpecificUserInfo(unittest.TestCase):

    def test_exist_usr(self):
        instance = GetSpecificUserInfo('aa')
        ret = instance.main()
        self.assertEqual(True, ret)

    def test_not_exist_usr(self):
        instance = GetSpecificUserInfo('Satoru_191')
        ret = instance.main()
        self.assertEqual(False, ret)


if __name__ == '__main__':
    unittest.main()