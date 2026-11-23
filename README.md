# bike-route-quality

Learn how good a street is for cycling from aerial and street level images
Goal: Build a labeled dataset and train a model that scores street segments


**Status: scaffolded** There is no data and there are no results yet. 
The model, loss, training, and tests run on synthetic data. The data collection modules are currently stubs.

## Overview

For each street segment the model reads in two views:

- an **aerial crop**, which shows the layout (lane width and buffer space) and
- a **street level photo**, which shows what the aerial images might miss (physical barriers, parked cars, surface condition, etc)

It predicts a **stress level** from 1 (comfortable) to 4 (stressful), following the
city of Boston's **Bicycle Level of Traffic Stress (BLTS)** scale, and a continuous quality score.
We are partly seeking to answer the question: **does imagery tell us something about cycling quality that map tags alone cannot?** 
A model that only relearns the tag rules would not be useful, so a tag only
baseline comes first and the image model must beat this baseline on neighborhoods it has never seen in training. For this, we leave out entire neighborhoods of Boston from the training set to avoid the model scoring well on similar nearby streets from its training data. Streets in Allston look markedly different from those in Somerville, for example, and we want the model to provide accurate scores on both. 

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest                      # runs on synthetic data for now
```

Training needs a segment table (see `src/bikeroute/schema.py` and `data/README.md`):

```bash
python -m bikeroute.train --config configs/default.yaml
```

Data collection needs extra packages: `pip install -e ".[geo]"`.

## Layout

```
configs/default.yaml        training settings
data/                       local data, not committed (see data/README.md)
src/bikeroute/
  schema.py                 column names of the segment table
  dataset.py                segment table -> training examples
  splits.py                 hold out whole neighborhoods for testing
  model.py                  two image encoders + shared head
  losses.py                 stress level loss + quality score loss
  train.py                  training and evaluation loops
  sources/                  data collection (stubs)
tests/                      run on synthetic images
```

## Plan

- Collect street segments, aerial crops, street level photos, labels
- Hand audit a sample of a few hundred segments
- Get the tag only baseline
- Train the image model; evaluate performance on held out neighborhoods
- Explain predictions with Grad-CAM (highlights the image regions that caused a score)
- Audit segments where the model and the stress ratings disagree
- Write up and release the dataset pipeline for other cities

## Data and attribution

Planned sources: OpenStreetMap, MassGIS aerial imagery, Mapillary street-level photos
(CC BY-SA 4.0, attribution required), MassDOT and City of Boston bike facility data,
Boston Vision Zero crash records, and stress ratings from the Boston Cyclists Union
Labs Bike Stress Map and the City of Boston Bicycle Level of Traffic Stress map.
Details and terms are in [`data/README.md`](data/README.md).

## Related work

- Hollander et al. (2021), [Using deep learning to examine the correlation between
  transportation planning and perceived safety of the built environment](https://journals.sagepub.com/doi/10.1177/2399808320959079)
- Sangers, van Gemert and van Cranenburgh (2022), [Explainability of deep learning
  models for urban space perception](https://arxiv.org/abs/2208.13555)
- Dubey et al. (2016), [Deep learning the city: Quantifying urban perception at a
  global scale](https://arxiv.org/abs/1608.01769)
- City of Boston, [Interactive Bicycle Stress Map](https://boston.maps.arcgis.com/apps/webappviewer/index.html?id=f0be9f03ada74a028cd05e4893a22ca4)

## Related codebases / codebases I found helpful for this implementation
- BCU's crash map (no longer actively maintained): [crash map repo](https://github.com/BostonCyclistsUnion/crash_map)
- BCU's stress map: [stress map repo](https://github.com/BostonCyclistsUnion/StressMap)

## Licence

MIT. See [LICENSE](LICENSE).
