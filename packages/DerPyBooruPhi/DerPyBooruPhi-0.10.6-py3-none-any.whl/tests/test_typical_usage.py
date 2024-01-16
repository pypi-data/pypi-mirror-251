import unittest
from derpibooru import Search, sort, query
from derpibooru.comment import Comment
from derpibooru.filters import Filter, system_filters
from derpibooru.image import Image
from derpibooru.profile import Profile
from derpibooru.tags import Tags

class TestTypicalUsage(unittest.TestCase):
    def test_getting_images(self):
        '''Getting images currently on Derpibooru's front page
        '''

        counter = 0
        for image in Search():
            counter += 1
            self.assertIsInstance(image.id, int)
            self.assertIsInstance(image.score, int)
            self.assertIsInstance(image.tags, list)
            id_number, score, tags = image.id, image.score, ", ".join(image.tags)
            print("#{} - score: {:>3} - {}".format(id_number, score, tags))
            if counter > 60:
                break
        print(counter)
        self.assertGreater(counter, 0)
        self.assertLessEqual(counter, 50)

    def test_searching(self):
        '''Searching posts by tag
        '''

        counter = 0
        for image in Search().query("rarity", "twilight sparkle"):
            counter += 1
            self.assertIn("rarity", image.tags)
            self.assertIn("twilight sparkle", image.tags)
            self.assertIsNotNone(image.url)
            self.assertEqual(image.url, f"https://derpibooru.org/images/{image.id}")
            print(image.url)
        self.assertGreater(counter, 0)

    def test_searching_other_booru(self):
        '''Getting images from other booru
        '''

        counter = 0
        for image in Search(url_domain='https://ponerpics.org').query("rarity", "twilight sparkle"):
            counter += 1
            self.assertIn("rarity", image.tags)
            self.assertIn("twilight sparkle", image.tags)
            self.assertIsNotNone(image.url)
            self.assertEqual(image.url, f"https://ponerpics.org/images/{image.id}")
            print(image.url)
        self.assertGreater(counter, 0)

    def test_get_random(self):
        '''Getting random posts
        '''

        counter = 0
        image_id = 0
        for image in Search().sort_by(sort.RANDOM):
            counter += 1
            self.assertNotEqual(image_id, image.id)
            image_id = image.id
            self.assertIsNotNone(image.url)
            self.assertEqual(image.url, f"https://derpibooru.org/images/{image.id}")
            print(image.url)
        self.assertGreater(counter, 0)

    def test_get_top(self):
        '''Getting top 100 posts
        '''

        top_scoring = [image.url for image in Search().sort_by(sort.SCORE).limit(100)]
        print(top_scoring)
        self.assertEqual(len(top_scoring), 100)

    def test_passing_new_parameters(self):
        '''Storing and passing new search parameters
        '''
        params = Search().sort_by(sort.SCORE).limit(100).parameters
        print(params)

        top_scoring = Search(**params)
        self.assertDictEqual(params, top_scoring.parameters)
        top_animated = top_scoring.query("animated")
        print(top_animated.parameters)

        top = [image.url for image in top_animated]
        print(top)
        self.assertEqual(len(top), 50)

    def test_filtering_metadata(self):
        '''Filtering by metadata
        '''
        q = {
            "wallpaper",
            query.width == 1920,
            query.height == 1080,
            query.score >= 100
        }
        print(q)

        for qq in q:
            self.assertIsInstance(qq, str)

        wallpapers = [image.url for image in Search().query(*q)]
        print(wallpapers)
        self.assertEqual(len(wallpapers), 50)

    def test_get_image_by_id(self):
        '''Getting Image data by id
        '''
        i_want_ponies_ponified = Image(None,image_id=0)
        print(i_want_ponies_ponified.url)
        print(i_want_ponies_ponified.image)
        self.assertEqual(i_want_ponies_ponified.id, 0)
        self.assertEqual(i_want_ponies_ponified.url, "https://derpibooru.org/images/0")
        self.assertIsNotNone(i_want_ponies_ponified.image)

    def test_get_comments(self):
        '''Getting comments
        '''
        counter = 0
        for image in Search().query(query.id == 0):
            for comment in image.comments:
                print(f"{comment.author}: {comment.body}")
                counter += 1
        self.assertGreater(counter, 0)

    def test_get_comments_by_id(self):
        '''Getting comments by id
        '''
        which_video = Comment(None, comment_id=1000)
        print("Comment from",which_video.image_id)
        print(f"{which_video.author}: {which_video.body}")
        self.assertIsNotNone(which_video.author)
        self.assertIsNotNone(which_video.body)
        self.assertEqual(which_video.id, 1000)
        self.assertEqual(which_video.image_id, 454937)

    def test_tags(self):
        '''Tags
        '''
        tags = Tags("luna || twilight sparkle")
        parent = None
        for tag in tags:
            self.assertIsNotNone(tag)
            self.assertIsNotNone(tag.name)
            if tag.alias_parent():
                parent = tag.name, tag.alias_parent().name
            print(tag, tag.alias_parent())

        self.assertIsNotNone(parent)

        is_checked = False
        for tag in tags.query(parent[1]):
            self.assertIsNotNone(tag)
            self.assertIsNotNone(tag.name)
            print(tag, tag.alias_parent())
            for child in tag.alias_children():
                is_checked |= parent[0]==child.name
                print(tag, child)
        self.assertTrue(is_checked)

        is_checked = False
        for tag in tags.query("socks"):
            self.assertIsNotNone(tag)
            self.assertIsNotNone(tag.name)
            for child in tag.implied():
                is_checked |= "clothes"==child.name
                print(tag, child)
        self.assertTrue(is_checked)

        is_checked = False
        for tag in tags.query("socks"):
            self.assertIsNotNone(tag)
            self.assertIsNotNone(tag.name)
            for child in tag.implied_by():
                is_checked |= "socks only"==child.name
                print(tag, child)
        self.assertTrue(is_checked)

    def test_profiles(self):
        '''Profiles
        '''
        profile = Profile(216494)
        print(profile)
        self.assertIsNotNone(profile.name)

    def test_filters(self):
        '''Filters
        '''
        profile = Filter(system_filters['everything'])
        print(profile)
        self.assertEqual(profile.name, "Everything")

if __name__ == '__main__':
    unittest.main()
