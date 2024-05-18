# XVL -- a voxel file format

## File format

### Header

|Word|64-bit value                     |Meaning            |
|----|---------------------------------|-------------------|
|   0|`#VXLBIN\n`                      |Magic              |
|   1|`#000000\z`                      |Version            |
|   2|64-bit signed integer, big endian|X-resolution       |
|   3|64-bit signed integer, big endian|Y-resolution       |
|   4|64-bit signed integer, big endian|Z-resolution       |
|   5|IEEE double float                |X-length in [m]    |
|   6|IEEE double float                |Y-length in [m]    |
|   7|IEEE double float                |Z-length in [m]    |
|   8|String                           |Coordinate system  |
|   9|IEEE double float                |Longitude of origin|
|  10|IEEE double float                |Latitude of origin |
|  11|IEEE double float                |Elevation of origin|
|  12|                                 |Reserved           |
|  13|                                 |Reserved           |
|  14|                                 |Reserved           |
|  15|                                 |Reserved           |

### Body

Array of 8-bit signed integer (`char`).