#!/bin/bash

source="orthophotomosaic_CoralReef_reprojected.tif"

process()
{
    length="$1"
    format="$2"


    name="orthophotomosaic_curacao_${length}_${format}"
    folder="./output/${name}"
    echo "Processing ${name}"
    mkdir -p "$folder"

    # Creating intermediate image, if needed

    width=$(identify -format '%w' "$source")
    height=$(identify -format '%h' "$source")

    new_width=$((  $length * ($width / $length)  ))
    new_height=$(( $length * ($height / $length)  ))

    echo "  Resized image ${length}: ${width}x${height} -> ${new_width}x${new_height}"

    new="./temp/${source%%.*}-resized_for_${length}.${source##*.}"
    mkdir -p "$(dirname "$new")"
    if [ ! -e "$new" ]; then
        echo "  Creating intermediate resized image: ${new}"
        convert "$source" -gravity Center -crop "${new_width}x${new_height}+0+0" +repage "$new"
    fi

    # Creating tiles

    convert "$new" +gravity -crop "${length}x${length}" "${folder}/tile_%04d.${format}"
    total=$(ls -1 "$folder" | wc -l)
    tar -cjpf "${folder}-${total}_tiles.tar.bz2" "${folder}"
    echo "  completed ${name}"
}

clean()
{
    echo "Cleaning"
    if [ -e "./output/" ]; then
        rm -r ./output/
    fi
    if [ -e "./temp/" ]; then
        rm -r ./temp/
    fi
}

main()
{
    clean    

    for format in jpg tif
    do    
        for length in 256 512
        do
            process $length $format
        done
    done
}

main


