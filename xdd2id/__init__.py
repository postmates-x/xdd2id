import xml.etree.ElementTree as ET
from xml.dom import minidom

from ._ids import IDS_MAP


__version__ = '0.1.0'
""" str: Version. """


_VAR = '7'
""" str: CANopen object type, variable. """
_ARR = '8'
""" str: CANopen object type, array. """
_RECORD = '9'
""" str: CANopen object type, record. """

_DATA_TYPES = {
    '01': 'bool',
    '02': 's8',
    'USINT': 's8',
    '03': 's16',
    'INT': 's16',
    '04': 's32',
    'DINT': 's32',
    '05': 'u8',
    'SINT': 's8',
    '06': 'u16',
    'UINT': 'u16',
    '07': 'u32',
    'UDINT': 'u32',
    '08': 'float',
    '09': 'str',
    '0a': 'str',
    'STRING': 'str',
    '15': 's64',
    'LINT': 's64',
    '1b': 'u64',
    'ULINT': 'u64'
}
""" dict: Mapping for Supported CANopen data types. """

_ACCESS_TYPES = {
    'const': 'ro',
    'ro': 'ro',
    'read': 'ro',
    'rw': 'rw',
    'readWrite': 'rw',
    'write': 'wo'
}
""" dict: Mapping for Supported CANopen access types. """

_FW_VERSION_INDEX = "100a"
""" str: Firmware version register. """


def convert(f_in, f_out):
        """ Convert CANopen XDD to IngeniaDictionary.

            Args:
                f_in (str): CANopen XDD file.
                f_out (str): IngeniaDictionary output file.

            Raises:
                KeyError: If any uniqueID reference is missing
                ValueError: If any data or access type is unsupported.
        """

        xdd = ET.parse(f_in)

        # obtain all CANopen objects/subobjects
        objs = []
        for obj in xdd.findall('.//CANopenObject'):
            if obj.attrib['index'] == _FW_VERSION_INDEX:
                firmwareVersionNumber = obj.attrib['defaultValue']

            if obj.attrib['objectType'] == _VAR:
                obj.attrib['subIndex'] = '00'
                objs.append(obj)
            elif obj.attrib['objectType'] in (_ARR, _RECORD):
                for sobj in obj:
                    if sobj.attrib['subIndex'] == '00':
                        continue

                    sobj.attrib['index'] = obj.attrib['index']
                    sobj.attrib['name'] = (obj.attrib['name'] + ' - ' +
                                           sobj.attrib['name'])
                    objs.append(sobj)

        # fill registers array
        regs = []
        for obj in objs:
            index = obj.attrib['index']
            subIndex = obj.attrib['subIndex']
            name = obj.attrib['name']

            # obtain data type / access type (on parameters or the object)
            if 'uniqueIDRef' in obj.attrib:
                params = xdd.find(
                    './/parameterList/parameter[@uniqueID=\'{}\']'.format(
                        obj.attrib['uniqueIDRef']))

                if params is None:
                    raise KeyError('Missing object reference')

                accessType = params.attrib['access']

                dataType = ''
                for param in params:
                    if param.tag.isupper():
                        dataType = param.tag
            else:
                dataType = obj.attrib['dataType']
                accessType = obj.attrib['accessType']

            # convert data type/ access type
            if dataType not in _DATA_TYPES:
                raise ValueError('Unsupported data type ({})'.format(dataType))

            dataType = _DATA_TYPES[dataType]

            if accessType not in _ACCESS_TYPES:
                raise ValueError('Unsupported access type ({})'.format(
                    accessType))

            accessType = _ACCESS_TYPES[accessType]

            # obtain ID
            address = subIndex + index
            if address not in IDS_MAP:
                identifier = name.upper().replace(' ', '_').replace(' - ', '_')
                identifier = ''.join(x for x in identifier if x.isalpha())
            else:
                identifier = IDS_MAP[address]

            regs.append({
                'attrib': {
                    'id': identifier,
                    'address': address,
                    'dtype': dataType,
                    'access': accessType
                },
                'label': name
            })

        # create IngeniaDictionary
        idict = ET.Element('IngeniaDictionary')

        header = ET.SubElement(idict, 'Header')
        version = ET.SubElement(header, 'Version')
        version.text = '1'
        defaultLanguage = ET.SubElement(header, 'DefaultLanguage')
        defaultLanguage.text = 'en_US'

        body = ET.SubElement(idict, 'Body')
        device = ET.SubElement(body, 'Device', attrib={
                                    'name': 'Generic',
                                    'family': 'ECORE',
                                    'firmwareVersion': firmwareVersionNumber})

        registers = ET.SubElement(device, 'Registers')
        for reg in regs:
            register = ET.SubElement(registers, 'Register',
                                     attrib=reg['attrib'])

            labels = ET.SubElement(register, 'Labels')
            label = ET.SubElement(labels, 'Label', attrib={'lang': 'en_US'})
            label.text = reg['label']

        # write IngeniaDictionary
        idict = ET.tostring(idict, 'utf-8')
        idict = minidom.parseString(idict)
        idict = idict.toprettyxml(indent='  ')

        with open(f_out, 'w') as f:
            f.write(idict)
