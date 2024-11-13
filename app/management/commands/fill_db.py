from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, AnswerLike, QuestionLike
from faker import Faker
import random


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        fake = Faker()
        tags = []
        for i in range(ratio):
            random_tag = fake.unique.word()
            tag, created = Tag.objects.get_or_create(name=random_tag)
            tag.save()
            tags.append(tag)
        for i in range(ratio):
            username = fake.unique.user_name()
            email = fake.unique.email()
            password = fake.password(length=10)
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            profile = Profile(user=user, avatar=None)
            profile.save()

            for i in range(10):
                question = Question.objects.create(profile=profile, title=fake.sentence(nb_words=3),
                                                   text=fake.paragraph(nb_sentences=2))
                random_tags = random.sample(tags, random.randint(1, 3))
                print(random_tags)
                question.tags.set(random_tags)
                question.save()
                for i in range(10):
                    answer = Answer(text=fake.paragraph(nb_sentences=3), question=question)
                    answer.save()

        for i in range(1,ratio * 200):
            random_user = random.randint(1, ratio)
            random_ans = random.randint(1, ratio*100)
            random_ques = random.randint(1, ratio*10)
            if not QuestionLike.objects.filter(user_id=random_user, question_id=random_ques).exists():
                QuestionLike.objects.create(user_id=random_user, question_id=random_ques)

            if not AnswerLike.objects.filter(user_id=random_user, answer_id=random_ans).exists():
                AnswerLike.objects.create(user_id=random_user, answer_id=random_ans)

