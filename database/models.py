"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

import decimal
from datetime import datetime

from database import db
from database.model_exceptions import LatitudeValueError, LongitudeValueError


class ProtectedHumidity(db.Model):
    """
    A class that represents the ORM for a humidity reading.
    """
    __tablename__ = 'humidity'
    id = db.Column(db.BIGINT(), primary_key=True, autoincrement=True)
    value = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    value_units = db.Column(db.NVARCHAR(16), nullable=False)
    value_error_range = db.Column(db.DECIMAL(precision=7, scale=6), nullable=False, default=0.0)
    latitude_public = db.Column(db.DECIMAL(precision=8, scale=6), nullable=False)
    latitude = db.Column(db.DECIMAL(precision=8, scale=6), nullable=False)
    longitude_public = db.Column(db.DECIMAL(precision=9, scale=6), nullable=False)
    longitude = db.Column(db.DECIMAL(precision=9, scale=6), nullable=False)
    city = db.Column(db.NVARCHAR(64), nullable=False)
    province = db.Column(db.NVARCHAR(64), nullable=False)
    country = db.Column(db.NVARCHAR(64), nullable=False)
    elevation = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    elevation_units = db.Column(db.NVARCHAR(16), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,
                 value: decimal,
                 value_units: str,
                 value_error_range: decimal,
                 latitude: decimal,
                 longitude: decimal,
                 city: str,
                 province: str,
                 country: str,
                 elevation: decimal,
                 elevation_units: str,
                 timestamp: datetime,
                 id=None):
        """
        Humidity constructor.

        latitude -90 to 90. longitude -180 to 180.
        latitude_public -90 to 90. longitude_public -180 to 180.

        :rtype: ProtectedHumidity
        :type value: decimal
        :type value_units: str
        :type value_error_range: decimal
        :type latitude: decimal
        :type longitude: decimal
        :type city: str
        :type province: str
        :type country: str
        :type elevation: decimal
        :type elevation_units: str
        :type timestamp: datetime
        """
        super().__init__()

        # Test case for latitude and longitude value assertions
        if latitude < -90.0 or latitude > 90.0:
            raise LatitudeValueError('latitude out of range (-90 to 90)')

        if longitude < -180.0 or longitude > 180.0:
            raise LongitudeValueError('longitude out of range (-90 to 90)')

        if id is not None:
            self.id = id

        self.value = value
        self.value_units = value_units
        self.value_error_range = value_error_range
        self.latitude = latitude
        self.latitude_public = float(int(latitude * 1000)) / 1000
        self.longitude = longitude
        self.longitude_public = float(int(longitude * 1000)) / 1000
        self.city = city
        self.province = province
        self.country = country
        self.elevation = elevation
        self.elevation_units = elevation_units
        self.timestamp = timestamp

    def __repr__(self):
        """
        Return a string representation of the ProtectedHumidity object.

        :return: A string representation of the ProtectedHumidity object.
        """
        if self.id is None:
            return '<ProtectedHumidity: value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '           timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '           latitude: {latitude:f}\n' + \
                   '           latitude_public: {latitude_public:f}\n' + \
                   '           longitude: {longitude:f}>\n' + \
                   '           longitude_public: {longitude_public:f}>\n' + \
                   '           location: {city}, {province} {country}' + \
                   '           elevation: {elevation:f} {elevation_units}>'.format(
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude=self.latitude,
                       latitude_public=self.latitude_public,
                       longitude=self.longitude,
                       longitude_public=self.longitude_public,
                       city=self.city,
                       province=self.province,
                       country=self.country,
                       elevation=self.elevation,
                       elevation_units=self.elevation_units
                   )
        else:
            return '<ProtectedHumidity: id: {id)}\n' + \
                   '           value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '           timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '           latitude: {latitude:f}\n' + \
                   '           latitude_public: {latitude_public:f}\n' + \
                   '           longitude: {longitude:f}>\n' + \
                   '           longitude_public: {longitude_public:f}>\n' + \
                   '           location: {city}, {province} {country}' + \
                   '           elevation: {elevation:f} {elevation_units}>\n'.format(
                       id=str(self.id),
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude=self.latitude,
                       latitude_public=self.latitude_public,
                       longitude=self.longitude,
                       longitude_public=self.longitude_public,
                       city=self.city,
                       province=self.province,
                       country=self.country,
                       elevation=self.elevation,
                       elevation_units=self.elevation_units
                   )

    def __str__(self):
        return self.__repr__()


class PublicHumidity(db.Model):
    """
    A class that represents the ORM for a public humidity reading.
    """
    __tablename__ = 'humidity_public_view'
    id = db.Column(db.BIGINT(), primary_key=True, autoincrement=True)
    value = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    value_units = db.Column(db.NVARCHAR(16), nullable=False)
    value_error_range = db.Column(db.DECIMAL(precision=7, scale=6), nullable=False, default=0.0)
    latitude_public = db.Column(db.DECIMAL(precision=8, scale=6), nullable=False)
    longitude_public = db.Column(db.DECIMAL(precision=9, scale=6), nullable=False)
    city = db.Column(db.NVARCHAR(64), nullable=False)
    province = db.Column(db.NVARCHAR(64), nullable=False)
    country = db.Column(db.NVARCHAR(64), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,
                 value: decimal,
                 value_units: str,
                 value_error_range: decimal,
                 latitude_public: decimal,
                 longitude_public: decimal,
                 city: str,
                 province: str,
                 country: str,
                 timestamp: datetime,
                 id=None):
        """
        HumidityPublic constructor.

        :rtype: PublicHumidity
        :type value: decimal
        :type value_units: str
        :type value_error_range: decimal
        :type latitude_public: decimal
        :type longitude_public: decimal
        :type city: str
        :type province: str
        :type country: str
        :type timestamp: datetime
        """
        super().__init__()

        if id is not None:
            self.id = id

        self.value = value
        self.value_units = value_units
        self.value_error_range = value_error_range
        self.latitude_public = latitude_public
        self.longitude_public = longitude_public
        self.city = city
        self.province = province
        self.country = country
        self.timestamp = timestamp

    def __repr__(self):
        """
        Return a string representation of the public ProtectedHumidity object.

        :return: A string representation of the public ProtectedHumidity object.
        """
        if self.id is None:
            return '<PublicHumidity: value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '                 timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '                 latitude_public: {latitude_public:f}\n' + \
                   '                 longitude_public: {longitude_public:f}>\n' + \
                   '                 location: {city}, {province} {country}>'.format(
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude_public=self.latitude_public,
                       longitude_public=self.longitude_public,
                       city=self.city,
                       province=self.province,
                       country=self.country
                   )
        else:
            return '<PublicHumidity: id: {id)}\n' + \
                   '                 value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '                 timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '                 latitude_public: {latitude_public:f}\n' + \
                   '                 longitude_public: {longitude_public:f}>\n' + \
                   '                 location: {city}, {province} {country}>\n'.format(
                       id=str(self.id),
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude_public=self.latitude_public,
                       longitude_public=self.longitude_public,
                       city=self.city,
                       province=self.province,
                       country=self.country
                   )

    def __str__(self):
        return self.__repr__()


class ProtectedPressure(db.Model):
    """
    A class that represents the ORM for a pressure reading.
    """
    __tablename__ = 'pressure'
    id = db.Column(db.BIGINT(), primary_key=True, autoincrement=True)
    value = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    value_units = db.Column(db.NVARCHAR(16), nullable=False)
    value_error_range = db.Column(db.DECIMAL(precision=7, scale=6), nullable=False, default=0.0)
    latitude_public = db.Column(db.DECIMAL(precision=8, scale=6), nullable=False)
    latitude = db.Column(db.DECIMAL(precision=8, scale=6), nullable=False)
    longitude_public = db.Column(db.DECIMAL(precision=9, scale=6), nullable=False)
    longitude = db.Column(db.DECIMAL(precision=9, scale=6), nullable=False)
    city = db.Column(db.NVARCHAR(64), nullable=False)
    province = db.Column(db.NVARCHAR(64), nullable=False)
    country = db.Column(db.NVARCHAR(64), nullable=False)
    elevation = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    elevation_units = db.Column(db.NVARCHAR(16), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,
                 value: decimal,
                 value_units: str,
                 value_error_range: decimal,
                 latitude: decimal,
                 longitude: decimal,
                 city: str,
                 province: str,
                 country: str,
                 elevation: decimal,
                 elevation_units: str,
                 timestamp: datetime,
                 id=None):
        """
        Pressure constructor.

        latitude -90 to 90. longitude -180 to 180.
        latitude_public -90 to 90. longitude_public -180 to 180.

        :rtype: ProtectedPressure
        :type value: decimal
        :type value_units: str
        :type value_error_range: decimal
        :type latitude: decimal
        :type longitude: decimal
        :type city: str
        :type province: str
        :type country: str
        :type elevation: decimal
        :type elevation_units: str
        :type timestamp: datetime
        """
        super().__init__()

        # Test case for latitude and longitude value assertions
        if latitude < -90.0 or latitude > 90.0:
            raise LatitudeValueError('latitude out of range (-90 to 90)')

        if longitude < -180.0 or longitude > 180.0:
            raise LongitudeValueError('longitude out of range (-90 to 90)')

        if id is not None:
            self.id = id

        self.value = value
        self.value_units = value_units
        self.value_error_range = value_error_range
        self.latitude = latitude
        self.latitude_public = float(int(latitude * 1000)) / 1000
        self.longitude = longitude
        self.longitude_public = float(int(longitude * 1000)) / 1000
        self.city = city
        self.province = province
        self.country = country
        self.elevation = elevation
        self.elevation_units = elevation_units
        self.timestamp = timestamp

    def __repr__(self):
        """
        Return a string representation of the ProtectedPressure object.

        :return: A string representation of the ProtectedPressure object.
        """
        if self.id is None:
            return '<ProtectedPressure: value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '           timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '           latitude: {latitude:f}\n' + \
                   '           latitude_public: {latitude_public:f}\n' + \
                   '           longitude: {longitude:f}>\n' + \
                   '           longitude_public: {longitude_public:f}>\n' + \
                   '           location: {city}, {province} {country}' + \
                   '           elevation: {elevation:f} {elevation_units}>'.format(
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude=self.latitude,
                       latitude_public=self.latitude_public,
                       longitude=self.longitude,
                       longitude_public=self.longitude_public,
                       city=self.city,
                       province=self.province,
                       country=self.country,
                       elevation=self.elevation,
                       elevation_units=self.elevation_units
                   )
        else:
            return '<ProtectedPressure: id: {id)}\n' + \
                   '           value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '           timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '           latitude: {latitude:f}\n' + \
                   '           latitude_public: {latitude_public:f}\n' + \
                   '           longitude: {longitude:f}>\n' + \
                   '           longitude_public: {longitude_public:f}>\n' + \
                   '           location: {city}, {province} {country}' + \
                   '           elevation: {elevation:f} {elevation_units}>\n'.format(
                       id=str(self.id),
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude=self.latitude,
                       latitude_public=self.latitude_public,
                       longitude=self.longitude,
                       longitude_public=self.longitude_public,
                       city=self.city,
                       province=self.province,
                       country=self.country,
                       elevation=self.elevation,
                       elevation_units=self.elevation_units
                   )

    def __str__(self):
        return self.__repr__()


class PublicPressure(db.Model):
    """
    A class that represents the ORM for a public pressure reading.
    """
    __tablename__ = 'pressure_public_view'
    id = db.Column(db.BIGINT(), primary_key=True, autoincrement=True)
    value = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    value_units = db.Column(db.NVARCHAR(16), nullable=False)
    value_error_range = db.Column(db.DECIMAL(precision=7, scale=6), nullable=False, default=0.0)
    latitude_public = db.Column(db.DECIMAL(precision=8, scale=6), nullable=False)
    longitude_public = db.Column(db.DECIMAL(precision=9, scale=6), nullable=False)
    city = db.Column(db.NVARCHAR(64), nullable=False)
    province = db.Column(db.NVARCHAR(64), nullable=False)
    country = db.Column(db.NVARCHAR(64), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,
                 value: decimal,
                 value_units: str,
                 value_error_range: decimal,
                 latitude_public: decimal,
                 longitude_public: decimal,
                 city: str,
                 province: str,
                 country: str,
                 timestamp: datetime,
                 id=None):
        """
        PressurePublic constructor.

        :rtype: PublicPressure
        :type value: decimal
        :type value_units: str
        :type value_error_range: decimal
        :type latitude_public: decimal
        :type longitude_public: decimal
        :type city: str
        :type province: str
        :type country: str
        :type timestamp: datetime
        """
        super().__init__()

        if id is not None:
            self.id = id

        self.value = value
        self.value_units = value_units
        self.value_error_range = value_error_range
        self.latitude_public = latitude_public
        self.longitude_public = longitude_public
        self.city = city
        self.province = province
        self.country = country
        self.timestamp = timestamp

    def __repr__(self):
        """
        Return a string representation of the public ProtectedPressure object.

        :return: A string representation of the public ProtectedPressure object.
        """
        if self.id is None:
            return '<PublicPressure: value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '                 timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '                 latitude_public: {latitude_public:f}\n' + \
                   '                 longitude_public: {longitude_public:f}>\n' + \
                   '                 location: {city}, {province} {country}>'.format(
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude_public=self.latitude_public,
                       longitude_public=self.longitude_public,
                       city=self.city,
                       province=self.province,
                       country=self.country
                   )
        else:
            return '<PublicPressure: id: {id)}\n' + \
                   '                 value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '                 timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '                 latitude_public: {latitude_public:f}\n' + \
                   '                 longitude_public: {longitude_public:f}>\n' + \
                   '                 location: {city}, {province} {country}>\n'.format(
                       id=str(self.id),
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude_public=self.latitude_public,
                       longitude_public=self.longitude_public,
                       city=self.city,
                       province=self.province,
                       country=self.country
                   )

    def __str__(self):
        return self.__repr__()


class ProtectedTemperature(db.Model):
    """
    A class that represents the ORM for a temperature reading.
    """
    __tablename__ = 'temperature'
    id = db.Column(db.BIGINT(), primary_key=True, autoincrement=True)
    value = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    value_units = db.Column(db.NVARCHAR(16), nullable=False)
    value_error_range = db.Column(db.DECIMAL(precision=7, scale=6), nullable=False, default=0.0)
    latitude_public = db.Column(db.DECIMAL(precision=8, scale=6), nullable=False)
    latitude = db.Column(db.DECIMAL(precision=8, scale=6), nullable=False)
    longitude_public = db.Column(db.DECIMAL(precision=9, scale=6), nullable=False)
    longitude = db.Column(db.DECIMAL(precision=9, scale=6), nullable=False)
    city = db.Column(db.NVARCHAR(64), nullable=False)
    province = db.Column(db.NVARCHAR(64), nullable=False)
    country = db.Column(db.NVARCHAR(64), nullable=False)
    elevation = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    elevation_units = db.Column(db.NVARCHAR(16), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,
                 value: decimal,
                 value_units: str,
                 value_error_range: decimal,
                 latitude: decimal,
                 longitude: decimal,
                 city: str,
                 province: str,
                 country: str,
                 elevation: decimal,
                 elevation_units: str,
                 timestamp: datetime,
                 id=None):
        """
        ProtectedTemperature constructor.

        latitude -90 to 90. longitude -180 to 180.
        latitude_public -90 to 90. longitude_public -180 to 180.

        :rtype: ProtectedHumidity
        :type value: decimal
        :type value_units: str
        :type value_error_range: decimal
        :type latitude: decimal
        :type longitude: decimal
        :type city: str
        :type province: str
        :type country: str
        :type elevation: decimal
        :type elevation_units: str
        :type timestamp: datetime
        """
        super().__init__()

        # Test case for latitude and longitude value assertions
        if latitude < -90.0 or latitude > 90.0:
            raise LatitudeValueError('latitude out of range (-90 to 90)')

        if longitude < -180.0 or longitude > 180.0:
            raise LongitudeValueError('longitude out of range (-90 to 90)')

        if id is not None:
            self.id = id

        self.value = value
        self.value_units = value_units
        self.value_error_range = value_error_range
        self.latitude = latitude
        self.latitude_public = float(int(latitude * 1000)) / 1000
        self.longitude = longitude
        self.longitude_public = float(int(longitude * 1000)) / 1000
        self.city = city
        self.province = province
        self.country = country
        self.elevation = elevation
        self.elevation_units = elevation_units
        self.timestamp = timestamp

    def __repr__(self) -> str:
        """
        Return a string representation of the ProtectedTemperature object.

        :return: A string representation of the ProtectedTemperature object.
        """
        if self.id is None:
            return '<ProtectedTemperature: value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '              timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '              latitude: {latitude:f}\n' + \
                   '              latitude_public: {latitude_public:f}\n' + \
                   '              longitude: {longitude:f}>\n' + \
                   '              longitude_public: {longitude_public:f}>\n' + \
                   '              location: {city}, {province} {country}' + \
                   '              elevation: {elevation:f} {elevation_units}>'.format(
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude=self.latitude,
                       latitude_public=self.latitude_public,
                       longitude=self.longitude,
                       longitude_public=self.longitude_public,
                       city=self.city,
                       province=self.province,
                       country=self.country,
                       elevation=self.elevation,
                       elevation_units=self.elevation_units
                   )
        else:
            return '<ProtectedTemperature: id: {id)}\n' + \
                   '              value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '              timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '              latitude: {latitude:f}\n' + \
                   '              latitude_public: {latitude_public:f}\n' + \
                   '              longitude: {longitude:f}>\n' + \
                   '              longitude_public: {longitude_public:f}>\n' + \
                   '              location: {city}, {province} {country}' + \
                   '              elevation: {elevation:f} {elevation_units}>\n'.format(
                       id=str(self.id),
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude=self.latitude,
                       latitude_public=self.latitude_public,
                       longitude=self.longitude,
                       longitude_public=self.longitude_public,
                       city=self.city,
                       province=self.province,
                       country=self.country,
                       elevation=self.elevation,
                       elevation_units=self.elevation_units
                   )

    def __str__(self):
        return self.__repr__()


class PublicTemperature(db.Model):
    """
    A class that represents the ORM for a public temperature reading.
    """
    __tablename__ = 'temperature_public_view'
    id = db.Column(db.BIGINT(), primary_key=True, autoincrement=True)
    value = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    value_units = db.Column(db.NVARCHAR(16), nullable=False)
    value_error_range = db.Column(db.DECIMAL(precision=7, scale=6), nullable=False, default=0.0)
    latitude_public = db.Column(db.DECIMAL(precision=8, scale=6), nullable=False)
    longitude_public = db.Column(db.DECIMAL(precision=9, scale=6), nullable=False)
    city = db.Column(db.NVARCHAR(64), nullable=False)
    province = db.Column(db.NVARCHAR(64), nullable=False)
    country = db.Column(db.NVARCHAR(64), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,
                 value: decimal,
                 value_units: str,
                 value_error_range: decimal,
                 latitude_public: decimal,
                 longitude_public: decimal,
                 city: str,
                 province: str,
                 country: str,
                 timestamp: datetime,
                 id=None):
        """
        TemperaturePublic constructor.

        :rtype: PublicTemperature
        :type value: decimal
        :type value_units: str
        :type value_error_range: decimal
        :type latitude_public: decimal
        :type longitude_public: decimal
        :type city: str
        :type province: str
        :type country: str
        :type timestamp: datetime
        """
        super().__init__()

        if id is not None:
            self.id = id

        self.value = value
        self.value_units = value_units
        self.value_error_range = value_error_range
        self.latitude_public = latitude_public
        self.longitude_public = longitude_public
        self.city = city
        self.province = province
        self.country = country
        self.timestamp = timestamp

    def __repr__(self):
        """
        Return a string representation of the public ProtectedTemperature object.

        :return: A string representation of the public ProtectedTemperature object.
        """
        if self.id is None:
            return '<PublicTemperature: value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '                    timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '                    latitude_public: {latitude_public:f}\n' + \
                   '                    longitude_public: {longitude_public:f}>\n' + \
                   '                    location: {city}, {province} {country}>'.format(
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude_public=self.latitude_public,
                       longitude_public=self.longitude_public,
                       city=self.city,
                       province=self.province,
                       country=self.country
                   )
        else:
            return '<PublicTemperature: id: {id)}\n' + \
                   '                    value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '                    timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '                    latitude_public: {latitude_public:f}\n' + \
                   '                    longitude_public: {longitude_public:f}>\n' + \
                   '                    location: {city}, {province} {country}>\n'.format(
                       id=str(self.id),
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude_public=self.latitude_public,
                       longitude_public=self.longitude_public,
                       city=self.city,
                       province=self.province,
                       country=self.country
                   )

    def __str__(self):
        return self.__repr__()


class User(db.Model):
    """
    A class that represents the ORM for a user account.
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.NVARCHAR(64), nullable=False)
    password = db.Column(db.NVARCHAR(120), nullable=False)
    enabled = db.Column(db.BOOLEAN, nullable=False)
    created_date = db.Column(db.DATETIME, nullable=False, default=datetime.utcnow())
    last_login_date = db.Column(db.DATETIME, nullable=True)

    def __init__(self,
                 username: str,
                 password: str,
                 enabled: bool,
                 created_date: datetime = None,
                 last_login_date: datetime = None,
                 id=None):
        """
        User constructor.

        :param username: The user's username.
        :type username: str
        :param password: The user's SHA256 encrypted password.
        :type password: str
        :param enabled: Boolean indicating if the user is enabled for login.
        :type enabled: bool
        :param created_date: The date and time the user's account was created.
        :type created_date: datetime
        :param last_login_date: The date and time the user last logged in.
        :type last_login_date: datetime
        :param id: The database id for the user.
        :type id: int
        """
        super().__init__()

        if id is not None:
            self.id = id
        self.username = username
        self.password = password
        self.enabled = enabled
        self.created_date = created_date
        self.last_login_date = last_login_date

    def __repr__(self) -> str:
        """
        Return a string representation of the User object.

        :return: A string representation of the User object.
        """
        result = '<User: id: {id} username: {username}>'.format(
            id=str(self.id),
            username=self.username
        )
        return result

    def __str__(self):
        result = self.__repr__()
        return result
