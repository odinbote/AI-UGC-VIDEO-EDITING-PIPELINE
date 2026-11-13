(function () {
    app.beginUndoGroup("Complete 3D Horizontal Image Ring");

    var comp = app.project.activeItem;

    if (!(comp instanceof CompItem)) {
        alert("Open your composition first.");
        app.endUndoGroup();
        return;
    }

    var images = comp.selectedLayers;

    if (images.length !== 5) {
        alert("Select exactly 5 image layers in the timeline.");
        app.endUndoGroup();
        return;
    }

    // CUSTOM SETTINGS
    var radius = 700;
    var rotationDuration = 12;
    var imageScale = 35;
    var cameraZoom = 1800;
    var cameraDistance = 2200;

    var cx = comp.width / 2;
    var cy = comp.height / 2;

    // CREATE 3D CONTROLLER
    var ring = comp.layers.addNull();
    ring.name = "3D RING CONTROLLER";
    ring.threeDLayer = true;
    ring.property("Position").setValue([cx, cy, 0]);

    // ARRANGE FIVE IMAGES AROUND THE RING
    for (var i = 0; i < images.length; i++) {
        var layer = images[i];
        var angle = (i * 360 / images.length) * Math.PI / 180;

        var x = Math.sin(angle) * radius;
        var z = -Math.cos(angle) * radius;

        layer.threeDLayer = true;
        layer.parent = ring;

        layer.property("Anchor Point").setValue([
            layer.width / 2,
            layer.height / 2,
            0
        ]);

        layer.property("Position").setValue([x, 0, z]);
        layer.property("Scale").setValue([
            imageScale,
            imageScale,
            imageScale
        ]);

        // Each image faces outward from the center.
        layer.property("Orientation").setValue([
            0,
            i * 72,
            0
        ]);

        layer.property("X Rotation").setValue(0);
        layer.property("Y Rotation").setValue(0);
        layer.property("Z Rotation").setValue(0);
    }

    // CONTINUOUS RING ROTATION
    ring.property("Y Rotation").expression =
        "time * " + (360 / rotationDuration);

    // CREATE CAMERA
    var camera = comp.layers.addCamera(
        "3D RING CAMERA",
        [cx, cy]
    );

    camera.property("Position").setValue([
        cx,
        cy,
        -cameraDistance
    ]);

    camera.property("Point of Interest").setValue([
        cx,
        cy,
        0
    ]);

    camera.property("Camera Options")
        .property("Zoom")
        .setValue(cameraZoom);

    // PLACE CAMERA AND CONTROLLER ABOVE THE IMAGE LAYERS
    camera.moveToBeginning();
    ring.moveToBeginning();

    app.endUndoGroup();
    alert("5-image 3D ring created successfully.");
})();
