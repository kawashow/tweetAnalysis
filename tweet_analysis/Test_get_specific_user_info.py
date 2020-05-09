import unittest
from tweet_analysis.get_specific_user_info import GetSpecificUserInfo


class TestGetSpecificUserInfo(unittest.TestCase):

    def test_exist_usr(self):
        instance = GetSpecificUserInfo('aa')
        ret = instance.main()
        instance.output_csv()
        self.assertEqual(True, ret)

    def test_not_exist_usr(self):
        instance = GetSpecificUserInfo('Satoru_191')
        ret = instance.main()
        self.assertEqual(False, ret)

    def test_exist_usr_not_csv(self):
        instance = GetSpecificUserInfo('aa', to_csv=False)
        ret = instance.main()
        self.assertEqual([['id_str', 'tweet_text', 'favorite', 'RT', 'tweet_date', 'in_reply_to_status_id_str',
                           'media_id', 'media_url'], ['1212767867940343808',
                                                      "Damn, I was trying to tweet something important on the first day of the new decade. I guess I missed it, will have to wait until 2030.",
                                                      13, 2, '2020-01-03 01:09:26', None, '', '']], ret)


if __name__ == '__main__':
    unittest.main()
