import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Base,
    AdminLevelType,
    HazardType,
    HazardLevel,
    FeedbackStatus,
    #HazardCategory,
    #AdditionalInformationGroup,
    #AdditionalInformationType,
    #ReturnPeriod,
    #IntensityThreshold,
    )

from .. import load_local_settings


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    load_local_settings(settings)

    engine = engine_from_config(settings, 'sqlalchemy.')
    populate_db(engine)


def populate_db(engine):
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with transaction.manager:

        # AdditionalInformationGroup
        #for i in [
            #(u'BDG', u'Buildings', u'Buildings'),
            #(u'SCL', u'Social', u'Social'),
            #(u'INF', u'Infrastructure', u'Infrastructure'),
        #]:
            #r = AdditionalInformationGroup()
            #r.mnemonic, r.title, r.description = i
            #DBSession.add(r)

        ## AdditionalInformationType
        #for i in [
            #(u'REC', u'Recommendation', u'Recommendations'),
            #(u'RDA', u'Raw data', u'Raw data'),
            #(u'AVD', u'Added-value data', u'Added-value data'),
            #(u'PDF', u'PDF hazard report', u'Hazard report under Adobe PDF format'),  # noqa
        #]:
            #r = AdditionalInformationType()
            #r.mnemonic, r.title, r.description = i
            #DBSession.add(r)

        # FeedbackStatus
        for i in [
            (u'TBP', u'To be processed'),
            (u'PIP', u'Process in progress'),  # noqa
            (u'PRD', u'Process done'),
        ]:
            r = FeedbackStatus()
            r.mnemonic, r.title = i
            DBSession.add(r)

        # AdminLevelType
        for i in [
            (u'COU', u'Country', u'Administrative division of level 0'),
            (u'PRO', u'Province', u'Administrative division of level 1'),
            (u'REG', u'Region', u'Administrative division of level 2'),
        ]:
            r = AdminLevelType()
            r.mnemonic, r.title, r.description = i
            DBSession.add(r)

        # HazardLevel
        for i in [
            (u'HIG', u'High', 1),
            (u'MED', u'Medium', 2),
            (u'LOW', u'Low', 3),
            (u'NPR', u'Not previously reported', 4),  # noqa
        ]:
            r = HazardLevel()
            r.mnemonic, r.title, r.order = i
            DBSession.add(r)

        # HazardType
        for i in [
            (u'FL', u'Flood', 1),
            (u'EQ', u'Earthquake', 2),
            (u'DG', u'Drought', 3),
            (u'VA', u'Volcanic ash', 7),
            (u'CY', u'Cyclone', 4),
            (u'TS', u'Tsunami', 6),
            (u'SS', u'Storm surge', 5),
            (u'LS', u'Landslide', 8),
        ]:
            r = HazardType()
            r.mnemonic, r.title, r.order = i
            DBSession.add(r)

        ## ReturnPeriod
        #for i in [
            #(u'EQ250', u'250 years', u'Return period of 250 years for earthquake', u'EQ'),  # noqa
            #(u'EQ475', u'475 years', u'Return period of 475 years for earthquake', u'EQ'),  # noqa
            #(u'EQ2500', u'2500 years', u'Return period of 2500 years for earthquake', u'EQ'),  # noqa
            #(u'EQ>2500', u'Higher than 2500 years', u'Return period higher than 2500 years for earthquake', u'EQ'),  # noqa
            #(u'FL10', u'10 years', u'Return period of 10 years for flood', u'FL'),  # noqa
            #(u'FL50', u'50 years', u'Return period of 50 years for flood', u'FL'),  # noqa
            #(u'FL100', u'100 years', u'Return period of 100 years for flood', u'FL'),  # noqa
            #(u'FL>100', u'Higher than 100 years', u'Return period higher than 100 years for flood', u'FL'),  # noqa
        #]:
            #r = ReturnPeriod()
            #r.mnemonic, r.title, r.description, type_ = i
            #r.hazardtype = DBSession.query(HazardType) \
                #.filter(HazardType.mnemonic == type_) \
                #.one()
            #DBSession.add(r)

        #for i in [
        ## IntensityThreshold
            #(u'EQ_IT_1', u'Intensity threshold 1 for earthquake : PGA', 98.655, u'cm/s2', u'', u'EQ'),  # noqa
            #(u'EQ_IT_2', u'Intensity threshold 2 for earthquake : PGA', 0.1, u'g', u'', u'EQ'),  # noqa
            #(u'FL_IT_1', u'Intensity threshold 1 for flood', 5, u'dm', u'', u'FL'),  # noqa
            #(u'FL_IT_2', u'Intensity threshold 2 for flood', 0.5, u'm', u'', u'FL'),  # noqa
            #(u'CY_IT_1', u'Intensity threshold 1 for cyclone', 80, u'km/h', u'', u'CY'),  # noqa
        #]:
            #r = IntensityThreshold()
            #r.mnemonic, r.title, r.value, r.unit, r.description, type_ = i
            #r.hazardtype = DBSession.query(HazardType) \
                #.filter(HazardType.mnemonic == type_) \
                #.one()
            #DBSession.add(r)

    DBSession.remove()
