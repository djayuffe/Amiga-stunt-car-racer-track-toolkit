# Object / scenery audit — v3

The rendering paths split assets into different classes; they should not all be treated as polygon meshes.

* Track road, sides and barriers are true geometry assembled from transformed vertices and quadrilateral/polygon rendering.
* The opponent car is inserted into the track depth-ordering path (`renderOpponentCarIfAhead/Behind/Occluded` -> `renderOpponentCar`), so it warrants a separate geometry/data-flow extraction pass.
* The player's cockpit components are not the same kind of world 3D model: engine, exhausts, wheel/top pieces and boost flames are dispatched through `renderMaskedGraphicsObject`. Those should be extracted as masked graphics/sprites, not falsely exported as 3D meshes.
* Mountain horizon is generated from angle/shape-index tables and is another distinct asset class.

This distinction is important for a third-party editor: world track geometry, opponent/world objects, cockpit overlays, and horizon/background data need separate importers.
