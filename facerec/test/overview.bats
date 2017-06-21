#!/usr/bin/env bats

@test "Check that enrollment of the first subject succeeds" {
    run ./facerec enroll --subject "Ted Crilly" test/photos/ted1.gif test/photos/ted2.jpg test/photos/ted3.jpg
    [ "$status" = 0 ]
    [ "$output" = "Enrolled subject: 'Ted Crilly', number of faces: 3" ]
}

@test "Check that enrollment of the second subject succeeds" {
    run ./facerec enroll --subject "Dougal Mcguire" test/photos/dougal1.jpg test/photos/dougal2.jpg test/photos/dougal3.gif
    [ "$status" = 0 ]
    [ "$output" = "Enrolled subject: 'Dougal Mcguire', number of faces: 3" ]
}

@test "Check that we can recognize the first subject on the photo" {
    run ./facerec identify test/photos/photo1.jpg
    [ "$status" = 0 ]
    [ "$output" = "Subject 'Ted Crilly' is recognized with confidence 98.2978159334" ]
}

@test "Check that we can recognize first subject on the photo" {
    run ./facerec identify test/photos/photo1.jpg
    [ "$status" = 0 ]
    [ "$output" = "Subject 'Ted Crilly' is recognized with confidence 98.2978159334" ]
}

@test "Check that we can recognize second subject on the photo" {
    run ./facerec identify test/photos/photo2.gif
    [ "$status" = 0 ]
    [ "$output" = "Subject 'Dougal Mcguire' is recognized with confidence 78.5389835475" ]
}

@test "Check that we cannot recognize face on the photo of a fridge" {
    run ./facerec identify test/photos/fridge.jpg
    [ "$status" = 2 ]
    [ "$output" = "Face was not detected in the original image" ]
}

@test "Check that we cannot recognize face if subject was not enrolled" {
    run ./facerec identify test/photos/larry.jpg
    [ "$status" = 2 ]
    [ "$output" = "Unable to recognize the face" ]
}

@test "Check that we can get the codes of all enrolled subjects" {
    run ./facerec list
    [ "${lines[0]}" = "Dougal Mcguire" ]
    [ "${lines[1]}" = "Ted Crilly" ]
}
