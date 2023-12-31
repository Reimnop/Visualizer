# Visualizer

This Blender add-on allows you to create audio visualizations directly within Blender.

Took inspiration from [Bizualizer](https://github.com/doakey3/Bizualizer).

## Installation

1. **Download**: Clone or download the repository.
2. **Blender Add-On Installation**:
    - Open Blender (version 4.0+ only).
    - Go to `Edit` > `Preferences`.
    - Click on `Add-ons`.
    - Click `Install` and select the downloaded `.zip` file.
    - Activate the add-on by checking the box next to its name.

## Usage

1. **Open Blender**: Launch Blender in a new file.
2. **Access the add-on**: In the **Properties** panel, go to **Scene** tab. Expand **Visualizer**.
3. **Select an audio file**
4. **Select template bar object**: Select a template bar object so that the add-on can bake audio waves into.
5. **Select output collection**: Select a collection so that when the audio waves are baked, the new objects are copied into the collection.
6. **Enter F-Curve path**: Enter the path relative to the template object of the F-Curve where the audio wave for that bar will be baked into.
7. **(Optional) Select additional object and F-Curve**: You can bake the entire frequency range into any F-Curve in any object.
8. **Fiddle with the settings**: Go wild!

## Contributing

Contributions are welcome!

## License

This project is licensed under the [GPL 3 License](LICENSE).

## Acknowledgments

- Inspiration or credits to any resources, libraries, or individuals that contributed to this project.
