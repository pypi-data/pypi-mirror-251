# VDOT Calculator

A compact VDOT calculator adhering to the original Daniels Running Formula book.

## Status: Work in Progress

🚧 **Note: This project is currently under development.** 🚧

### Description

The VDOT Calculator project aims to provide a compact tool for calculating VDOT, following the principles outlined in the original Daniels Running Formula book.

### Features (Coming Soon)

- Calculate VDOT based on your running performance.


### Issues

If you encounter any issues or have suggestions, feel free to [open an issue](https://github.com/CassioMaciel/Daniels_Running_Formula/issues).

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Installation

```
$ python -m pip install vdot_calculator
```

### How to use

```
>>> import vdot_calculator as vdot
>>> import datetime
>>> time = datetime.time(minute=27, second=00)
>>> distance = 5000 # meters
>>> vdot.vdot_from_time_and_distance(time, distance)
34.96
```

```
>>> import vdot_calculator as vdot
>>> import datetime
>>> pace = datetime.time(minute=5, second=24)
>>> distance = 5000 # meters
>>> vdot.vdot_from_distance_and_pace(distance,pace)
34.96
```

```
>>> import vdot_calculator as vdot
>>> import datetime
>>> pace = datetime.time(minute=5, second=24)
>>> time = datetime.time(minute=27, second=00)
>>> vdot.vdot_from_distance_and_pace(time,pace)
34.96
```

### Contact

For questions or inquiries, you can contact the project maintainer:

- **Cássio Maciel Lemos**
  - Email: cassio.lemos@petrobras.com.br
