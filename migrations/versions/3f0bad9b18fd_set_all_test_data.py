"""set all test data

Revision ID: 3f0bad9b18fd
Revises: 93ff86dfa96c
Create Date: 2024-03-28 03:09:00.796476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f0bad9b18fd'
down_revision = '93ff86dfa96c'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO venues (name, address, city, state, phone, website, facebook_link,
            seeking_talent, seeking_description, image_link) VALUES ('The Musical Hop',
            '1015 Folsom Street', 'San Francisco', 'CA', '123-123-1234', 'https://www.themusicalhop.com',
            'https://www.facebook.com/TheMusicalHop', True,
            'We are on the lookout for a local artist to play every two weeks. Please call us.',
            'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
            ), ('The Dueling Pianos Bar', '335 Delancey Street', 'New York', 'NY', '914-003-1132',
            'https://www.theduelingpianos.com', 'https://www.facebook.com/theduelingpianos',
            False, NULL, 'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
            ), ('Park Square Live Music & Coffee', '34 Whiskey Moore Ave', 'San Francisco', 'CA',
            '415-000-1234', 'https://www.parksquarelivemusicandcoffee.com', 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
            False, NULL, 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80');
    """)
    op.execute("""
        INSERT INTO artists (name, city, state, phone, website, facebook_link,
        seeking_venue, seeking_description, image_link) VALUES ('Guns N Petals',
        'San Francisco', 'CA', '326-123-5000', 'https://www.gunsnpetalsband.com',
        'https://www.facebook.com/GunsNPetals', True, 'Looking for shows to perform at in the San Francisco Bay Area!',
        'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
        ),('Matt Quevedo', 'New York', 'NY', '300-400-5000', NULL, 'https://www.facebook.com/mattquevedo923251523',
        False, NULL, 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
        ), ('The Wild Sax Band', 'San Francisco', 'CA', '432-325-5432', NULL, NULL, False,
        NULL, 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80');
    """)
    op.execute("""
        INSERT INTO shows (venue_id, artist_id, start_time) VALUES (
        1, 1, TO_TIMESTAMP('2019-05-21 21:30:00', 'YYYY-MM-DD HH24:MI:SS')),
        (3, 2, TO_TIMESTAMP('2019-06-15 23:00:00', 'YYYY-MM-DD HH24:MI:SS')),
        (3, 3, TO_TIMESTAMP('2035-04-01 20:00:00', 'YYYY-MM-DD HH24:MI:SS')),
        (3, 3, TO_TIMESTAMP('2035-04-08 20:00:00', 'YYYY-MM-DD HH24:MI:SS')),
        (3, 3, TO_TIMESTAMP('2035-04-15 20:00:00', 'YYYY-MM-DD HH24:MI:SS'));
    """)
    op.execute("""
        INSERT INTO artist_genre (artist_id, genre) VALUES (1, 'Rock n Roll'::genre), (2, 'Jazz'::genre), (3, 'Jazz'::genre), (3, 'Classical'::genre);
    """)
    op.execute("""
        INSERT INTO venue_genre (venue_id, genre) VALUES (1, 'Jazz'::genre), (1,'Reggae'::genre), (1,'Swing'::genre), (1,'Classical'::genre), (1,'Folk'::genre),
            (2,'Classical'::genre), (2,'R&B'::genre), (2,'Hip-Hop'::genre), (3,'Rock n Roll'::genre), (3,'Jazz'::genre), (3,'Classical'::genre), (3,'Folk'::genre);
    """)


def downgrade():
    op.execute("""
        DELETE FROM artist_genre;
    """)
    op.execute("""
        DELETE FROM venue_genre;
    """)
    op.execute("""
        DELETE FROM shows;
    """)
    op.execute("""
        DELETE FROM venues;
    """)
    op.execute("""
        DELETE FROM artists;
    """)
