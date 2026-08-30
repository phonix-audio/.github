# Phonix Audio

Instruments built from the physics and the literature, each one a VST3 and CLAP
plugin in its own repository, and a sequencer that hosts them.

## The principle

**The instrument is the interface.** An editor is a drawing of the object it
models, and its parts are the controls: the microphones on a piano's soundboard
are dots you drag, because that is where the model listens; a modulation route
is a pin in a hole on a patchboard, its cap saying what the route does and its
brightness how much. What the instrument does not have goes in an outboard
cluster that says so.

Two rules carry most of it. **Draw what the thing carries**: a note holds a
velocity and a probability, a step holds a condition and three alternate
pitches, and a control draws each of them. **Every forward map needs its
inverse, round-trip tested**: that is what makes a drawn shape a control rather
than a picture.

## The sequencer

[**aethon**](../../aethon) hosts every plugin here, plus the ones that live
inside it. Tracks, patterns, a clip launcher, an arrangement, a mixer with
group buses and sends, and a modulation matrix that reaches any parameter of
any track.

## The instruments

**Physical models.** The string, the bore and the plate are simulated, and the
decay, the beating of a unison and the resonance are consequences of that chain
rather than settings inside it.

| | |
|---|---|
| [cordis](../../cordis) | a grand piano: hammer against string, coupled unisons, soundboard in the loop |
| [archet](../../archet) | bowed strings and harpsichord: a friction junction on a waveguide, through a modal body |
| [souffle](../../souffle) | wind and brass: a bore delay line with a reed or lip at one end |
| [guitar](../../guitar) | electric guitar, with its amplifier and cabinet |
| [bass](../../bass) | electric bass, with slap, pick and distortion |
| [orgue](../../orgue) | a tonewheel drawbar organ, nine additive partials a voice, through a Leslie |

**Emulations.** Machines whose character is their own signal path.

| | |
|---|---|
| [tb303](../../tb303) | an acid bassline synthesizer with its own step sequencer |
| [vcs3](../../vcs3) | a semi-modular monosynth whose personality is its pin matrix |
| [vp330](../../vp330) | the Roland VP-330 Vocoder Plus: paraphonic strings, choir, vocoder |
| [mellotron](../../mellotron) | a tape-replay keyboard, eight seconds of tape a key |

**Synthesizers.**

| | |
|---|---|
| [polaris](../../polaris) | virtual analog: two oscillators with hard sync, a ladder filter |
| [solstice](../../solstice) | four FM operators into a free routing matrix, then an analog pair |
| [pulsar](../../pulsar) | wavetable, with unison and a modulation matrix |
| [strata](../../strata) | four synthesis engines blended in one voice |
| [magma](../../magma) | techno bass and lead: two wavetables, a shaper, a ducker |
| [atmosphera](../../atmosphera) | an ambient pad that moves on its own |
| [aurora](../../aurora) | cinematic evolving pads, four layers a voice |
| [nebula](../../nebula) | eight autonomous layers, generative rather than played |
| [grain](../../grain) | granular: a held note spawns a stream of windowed grains |
| [spectral](../../spectral) | a sound analysed into partials, resynthesised and reshaped |
| [sampler](../../sampler) | SFZ multisample playback, its key and velocity map drawn as the panel |

**Drums.**

| | |
|---|---|
| [techno-kick](../../techno-kick) | a kick designer: a pitched sine, a click, a compressor and a limiter |
| [drum-machine](../../drum-machine) | a drum machine with its own step sequencer |
| [plexus](../../plexus) | a generative drum machine |

**Voice.** Formant and diphone synthesis, and one processor of a real one.

| | |
|---|---|
| [singer](../../singer) | a singing voice, from text and a melody |
| [chorale](../../chorale) | an MBROLA diphone choir |
| [loquace](../../loquace) | formant synthesis, a talkbox and a vocoder |
| [aria](../../aria) | an operatic solo voice, FOF granular |
| [trancevoice](../../trancevoice) | a trance choir |
| [harmonizer](../../harmonizer) | a real-time vocal harmonizer, pitch-tracked and scale-aware |

**Effects.**

| | |
|---|---|
| [fx-rack](../../fx-rack) | an eight-slot stereo chain, the same effects the sequencer's inserts use |

## How they hold together

Seven crates are shared and never copied: the lock-free meter channel, the DSP
primitives, the saved-document types, the effects, the preset trait, the widget
library and the effect editors. One copy of a filter means one sound; two copies
drift, and a drifting filter changes every preset that uses it.

Each plugin pins what it cannot change: the class ids other programs resolve it
by, the parameter ids a host stores automation against, the serde field names,
the factory bank's names and order, and a hash over rendered audio. Each of
those has a test.
