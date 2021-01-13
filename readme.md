# kivy-tkinter
Run some simple Kivy and KV code purely using the Tkinter framework!

Use Tkinter using the Kivy coding style and the declarative KV language
with no changes to your Kivy project's code (If it doesn't run, this
project should change rather than your code--see "Development").

## Why?

Kivy is useful for deploying to desktops, but doing so requires a
virtualenv or a Python-to-binary tool. Upgrading to the next major
release of your distro usually breaks the virtualenv. Utilizing kivy-tkinter, the
problem goes away as no virtualenv nor compilation is necessary. It uses its own
subclasses of tkinter widgets. Note that only a subset of Kivy widgets
are implemented so far.

It is tkinter using kivy coding style and KV.

@tshirtman asks (Kivy discord channel #your-projects 2021-01-04), "did
you have a look at enaml-native? it's kind of like kvlang (though the
language seems a bit more noisy/messy to me), using native widgets, i
never tried it, though"

My main aim in this case is to provide a new "target" for Kivy apps
with no code change (See "Examples"). I may expand it when I run into
another one of my Kivy apps with the same situation, where I want
lightweight and platform-agnostic distribution and don't need advanced
graphical features of Kivy (Though kivy-tkinter could wrap those
features later).

The kivy-tkinter "target" for Kivy provides exceptional speed and
utilizes native or native-style widgets to the extent that Tkinter does.

Launch times for IntroCompatiblizer using 1 TB WD Black HDD (WD1003FZEX):
- Kivy
  - 1st launch: ~8s
  - 2nd launch: ~2s
- kivy-tkinter:
  - 1st launch ~3s
  - 2nd launch ~1s

(Times are approximate.) That difference is expected, because it
doesn't load any multimedia support, nor load a custom widget system.


## KivyMD Status
No project like kivymd-tkinter exists yet, but that is the recommended
approach.

Since KivyMD customizes widgets heavily, the most elegant (though not
actually "material design" (MD) unless the Tkinter theme is so)
solution for KivyMD compatibility is to create a kivymd-tkinter project
that subclasses kivy-tkinter widgets. For example, utilizing ttk's
Notebook for KivyMD tabs (or Kivy Carousel) is closer to the goals of
this project than implementing low-level widget drawing and gestures.

## Usage
Link or copy the kivy-tkinter/kivy directory into your app.

To link:
```
# set APP_DIR to your app's directory before running this code.
mkdir -p ~/git
cd ~/git && git clone https://github.com/poikilos/kivy-tkinter kivy-tkinter
cd $APP_DIR
ln -s ~/git/kivy-tkinter/kivy
```

Then run your app on a system or virtualenv that does not have Kivy, or
otherwise coerce Python to use the directory above rather than your
Kivy. If you aren't sure which is running, see the differences in the
theme as seen in the screenshots.

### Troubleshooting
- Doesn't Open

  If the app doesn't open, try running it from a command line interface
  to see the output.

- `NotImplementedError` (and most cases of `AttributeError` that don't
  occur when you run your code in Kivy):

  There is much to do to implement features like InstructionGroup,
  ListAdapter, and formats (images, videos etc), so if you need a
  feature like that, chances are you will have to code it yourself.
  Please submit changes in the form of a pull request due to the amount
  of work necessary to make this project "complete". I hope you enjoy
  this and contribute so that we can improve this project together.


## Examples
Kivy programs need no code changes to utilize kivy-tkinter! However,
only so many features of Kivy are implemented. Known working Kivy
apps include:

### [IntroCompatiblizer](https://github.com/poikilos/IntroCompatiblizer)

#### Before (Kivy)
![IntroCompatiblizer before](doc/images/IntroCompatiblizer-before.png)

#### After (kivy-tkinter)
![IntroCompatiblizer after](doc/images/IntroCompatiblizer-after.png)

## Development
See [contributing.md](contributing.md)

## Links
- [kivy-tkinter on Reddit](https://www.reddit.com/r/kivy/comments/kqh0gl/kivytkinter_a_wip_compatibility_layer_to_run_kivy/)
- [kivy-tkinter on kivy-users](https://groups.google.com/g/kivy-users/c/um19B__0ArU) on Google Groups
- [poikilos.org](https://poikilos.org) dev blog
- [kivy-tkinter on kivy General #your-projects](https://discord.com/channels/423249981340778496/498526835337068581/795768163932569652) on Discord
