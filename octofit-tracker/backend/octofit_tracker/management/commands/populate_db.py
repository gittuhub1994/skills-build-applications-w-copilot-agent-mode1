from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index and collection creation
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        # Force create all collections
        db.create_collection('users', capped=False) if 'users' not in db.list_collection_names() else None
        db.create_collection('teams', capped=False) if 'teams' not in db.list_collection_names() else None
        db.create_collection('activities', capped=False) if 'activities' not in db.list_collection_names() else None
        db.create_collection('workouts', capped=False) if 'workouts' not in db.list_collection_names() else None
        db.create_collection('leaderboard', capped=False) if 'leaderboard' not in db.list_collection_names() else None
        db.users.create_index('email', unique=True)

        # Clear all data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        tony = User.objects.create(email='tony@stark.com', name='Tony Stark', team=marvel)
        steve = User.objects.create(email='steve@rogers.com', name='Steve Rogers', team=marvel)
        bruce = User.objects.create(email='bruce@wayne.com', name='Bruce Wayne', team=dc)
        clark = User.objects.create(email='clark@kent.com', name='Clark Kent', team=dc)

        # Create activities
        Activity.objects.create(user=tony, type='Run', duration=30, date='2023-01-01')
        Activity.objects.create(user=steve, type='Swim', duration=45, date='2023-01-02')
        Activity.objects.create(user=bruce, type='Bike', duration=60, date='2023-01-03')
        Activity.objects.create(user=clark, type='Yoga', duration=20, date='2023-01-04')

        # Create workouts
        w1 = Workout.objects.create(name='Super Strength', description='Strength workout for heroes')
        w2 = Workout.objects.create(name='Flight Training', description='Aerobic workout for flyers')
        w1.suggested_for.set([tony, bruce])
        w2.suggested_for.set([steve, clark])

        # Create leaderboard
        Leaderboard.objects.create(user=tony, score=100)
        Leaderboard.objects.create(user=steve, score=90)
        Leaderboard.objects.create(user=bruce, score=95)
        Leaderboard.objects.create(user=clark, score=98)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
