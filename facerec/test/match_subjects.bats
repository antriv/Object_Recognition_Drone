#!/usr/bin/env bats

@test "Compare two images of the same subject succeeds" {
    run ./facerec compare test/photos/dougal3.gif test/photos/photo2.gif
    [ "$status" = 0 ]
    [ "$output" = "Match with confidence '64.6777569774'" ]
}

@test "Compare two images of different subjects exits with status 2" {
    run ./facerec compare test/photos/dougal2.jpg test/photos/ted1.gif
    [ "$status" = 2 ]
    [ "$output" = "Not match" ]
}

@test "Compare few images with one more image of the same subject succeeds" {
    run ./facerec compare test/photos/dougal2.jpg test/photos/dougal3.gif test/photos/photo2.gif
    [ "$status" = 0 ]
    [ "$output" = "Match with confidence '64.6777569774'" ]
}
