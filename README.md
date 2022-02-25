# Course Registration System
This repository contains codes and presentation slides for 2021 Fall CS489 Project.

## Project Description
At KAIST, we register our courses using random course registration systems. However, randomness make inevitable situations where students fail to take the compulsory lectures for graduation or miss the courses that they really want to take. However, the random system does not only engenders inconvenience, but also the ethical issues like buying or selling their course slots and using macro programs. A more complex program is necessary.

Thus, this CS489 project is about a more **concrete course registration system**. In this project, we will first simulate current registration situations happening at KAIST every semester. We will simulate the currently provided courses in all sorts: competitive and non-competitive in terms of capacity, compulsory or elective, basics or graduate-levels. Next, we will simulate students' desired course timetable based on real data. We hope to get some data on students’ initial preference on courses from course registration office at KAIST, but if not, we will simulate the student entities with qualitative surveys.

See the [project proposal slides](https://docs.google.com/presentation/d/1MvKQQvWTKKgcyD6869hr5r5vR4arvo9qF2p6UIif7Fk/edit?usp=sharing) for overall information about the project. Also, check [final project presentation](https://docs.google.com/presentation/d/155Qu70wGUpjCSIVYEWW6HJPv-ysM5eEDwgU6xxe-THE/edit?usp=sharing) and [final project paper](https://drive.google.com/file/d/1l-Rk86h2sto0e8lZHAjSE27HLrNK7gRb/view?usp=sharing) for in-depth discussions about this project.

## Tech Stack
We implemented all of our systems using a programming language Python. On top of it, we used various libraries to make registration system models and run experiments. Specific names of libraries are written in `requirements.txt`. We used
- `pandas`
- `openpyxl`
- `matplotlib`
- `numpy`
- `ipykernal`

## Experiment
By a written oath that our team took with KAIST Academic Registrar Team, we cannot share any data to run the model. Therefore, we remained all of the logs and plots from experiments that we did throughout the project in `visualization/visualize.ipynb`.

## Contribution
### Contributors
- [Jungeun Kim](https://github.com/jjungkang2)
- [Jinhee Yoo](https://github.com/jinhee-yoo)
- [Yeji Han](https://github.com/yj-han)
- [Jisu Yim](https://github.com/yimjisu)

### Branch and PR
- Use branches to implement one feature
- Ask for a PR to `main` branch when the implementation is done

### Commit Message Format
```
Commit Message

Done
- task 1
- task 2
- ...  
```
