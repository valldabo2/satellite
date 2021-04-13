from datetime import datetime

from project.models.fire import Fire

COLUMNS = [Fire.location.name, Fire.url.name, Fire.latitude.name, Fire.longitude.name,
           Fire.processing_date.name, Fire.confidence_level.name]

FAKE_DATA = [
    ['California', 'https://cdn.mos.cms.futurecdn.net/fzY6Emc4zDmXjwTqxMoZBL-1024-80.jpg.webp', 38.575764, -121.478851,
     datetime.today(), 99.2],
    ['Australia', 'https://cdn.governmentnews.com.au/wp-content/uploads/2015/09/31102243/BoM.jpg', -25.274398,
     133.775136, datetime.today(), 94.2],
    ['Japan', 'http://images.spaceref.com/news/2016/esa_earth_from_space_Japan_112516_945.jpg', 35.652832, 139.839478,
     datetime.today(), 92.2],
]
