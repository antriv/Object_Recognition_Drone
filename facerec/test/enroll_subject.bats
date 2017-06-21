#!/usr/bin/env bats

@test "Enrollment of the first subject with valid images succeeds" {
    run ./facerec enroll --subject "Ted Crilly" test/photos/ted1.gif test/photos/ted2.jpg test/photos/ted3.jpg
    [ "$status" = 0 ]
    [ "$output" = "Enrolled subject: 'Ted Crilly', number of faces: 3" ]
}

@test "Enrollment of the second subject with valid images succeeds" {
    run ./facerec enroll --subject "Dougal Mcguire" test/photos/dougal1.jpg test/photos/dougal2.jpg test/photos/dougal3.gif
    [ "$status" = 0 ]
    [ "$output" = "Enrolled subject: 'Dougal Mcguire', number of faces: 3" ]
}

@test "Enrollment of the subject without images fails with status 2" {
    run ./facerec enroll --subject "Jessup"
    [ "$status" = 2 ]
}

@test "Enrollment of the subject with invalid image path fails with status 1" {
    run ./facerec enroll --subject "Tom" test/photos/tom.jpg test/photos/tom2.jpg
    [ "$status" = 1 ]
    [ "$output" = "facerec: error: File not found: 'test/photos/tom2.jpg'" ]
}

@test "Enroll subject to the custom storage" {
    run ./facerec enroll --subject "Ted" --storage "/tmp/subjects" test/photos/ted1.gif test/photos/ted2.jpg
    [ "$status" = 0 ]
    [ "$output" = "Enrolled subject: 'Ted', number of faces: 2" ]
}
