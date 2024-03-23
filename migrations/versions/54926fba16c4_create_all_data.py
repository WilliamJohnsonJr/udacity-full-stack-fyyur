"""create all data

Revision ID: 54926fba16c4
Revises: ba1557553bb0
Create Date: 2024-03-22 19:36:46.382897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54926fba16c4'
down_revision = 'ba1557553bb0'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO venues (id, name, address, city, state, phone, website, facebook_link,
            seeking_talent, seeking_description, image_link) VALUES (1, 'The Musical Hop',
            '1015 Folsom Street', 'San Francisco', 'CA', '123-123-1234', 'https://www.themusicalhop.com',
            'https://www.facebook.com/TheMusicalHop', True,
            'We are on the lookout for a local artist to play every two weeks. Please call us.',
            'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
            ), (2, 'The Dueling Pianos Bar', '335 Delancey Street', 'New York', 'NY', '914-003-1132',
            'https://www.theduelingpianos.com', 'https://www.facebook.com/theduelingpianos',
            False, NULL, 'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
            ), (3, 'Park Square Live Music & Coffee', '34 Whiskey Moore Ave', 'San Francisco', 'CA',
            '415-000-1234', 'https://www.parksquarelivemusicandcoffee.com', 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
            False, NULL, 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80');
    """)
    op.execute("""
        INSERT INTO artists (id, name, city, state, phone, website, facebook_link,
        seeking_venue, seeking_description, image_link) VALUES (4, 'Guns N Petals',
        'San Francisco', 'CA', '326-123-5000', 'https://www.gunsnpetalsband.com',
        'https://www.facebook.com/GunsNPetals', True, 'Looking for shows to perform at in the San Francisco Bay Area!',
        'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
        ),(5, 'Matt Quevedo', 'New York', 'NY', '300-400-5000', NULL, 'https://www.facebook.com/mattquevedo923251523',
        False, NULL, 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
        ), (6, 'The Wild Sax Band', 'San Francisco', 'CA', '432-325-5432', NULL, NULL, False,
        NULL, 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80');
    """)
    op.execute("""
        INSERT INTO shows (id, venue_id, artist_id, start_time) VALUES (1,
        1, 4, TO_TIMESTAMP('2019-05-21 21:30:00', 'YYYY-MM-DD HH24:MI:SS')),
        (2, 3, 5, TO_TIMESTAMP('2019-06-15 23:00:00', 'YYYY-MM-DD HH24:MI:SS')),
        (3, 3, 6, TO_TIMESTAMP('2035-04-01 20:00:00', 'YYYY-MM-DD HH24:MI:SS')),
        (4, 3, 6, TO_TIMESTAMP('2035-04-08 20:00:00', 'YYYY-MM-DD HH24:MI:SS')),
        (5, 3, 6, TO_TIMESTAMP('2035-04-15 20:00:00', 'YYYY-MM-DD HH24:MI:SS'));
    """)
    op.execute("""
        INSERT INTO genres (id, name) VALUES (1, 'Jazz'), (2, 'Reggae'), (3, 'Swing'),
            (4, 'Classical'), (5, 'Folk'), (6, 'R&B'), (7, 'Hip-Hop'), (8, 'Rock n Roll');
    """)
    op.execute("""
        INSERT INTO artist_genre (artist_id, genre_id) VALUES (4, 8), (5, 1), (6, 1), (6, 4);
    """)
    op.execute("""
        INSERT INTO venue_genre (venue_id, genre_id) VALUES (1, 1), (1,2), (1,3), (1,4), (1,5),
            (2,4), (2,6), (2,7), (3,8), (3,1), (3,4), (3,5);
    """)



def downgrade():
    op.execute("""
        DELETE FROM artist_genre;
    """)
    op.execute("""
        DELETE FROM venue_genre;
    """)
    op.execute("""
        DELETE FROM genres;
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