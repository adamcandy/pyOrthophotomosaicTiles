#!/bin/bash

process()
{
    length="$1"
    format="$2"


    fullname="${name}_${length}_${format}"
    folder="./output/${fullname}"
    echo "Processing ${fullname}"
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

    total=$(( ($new_width / $length) * ($new_height / $length)  ))

    archive="${folder}-${total}_tiles.tar.bz2"
    if [ ! -e "${archive}" ]; then 
        echo "  Creating tiles: ${folder}/tile_%04d.${format} for archive: ${archive}"
        convert "$new" +gravity -crop "${length}x${length}" "${folder}/tile_%04d.${format}"
        total=$(ls -1 "$folder" | wc -l)
        # Check totals match here?
        echo "  Creating archive: ${archive}"
        tar --transform='s,./[^/]*/,,' -cjpf "${archive}" "${folder}"
        rm -r "${folder}"
    fi
    if [ -e "${folder}" ]; then 
        rm -r "${folder}"
    fi
    echo "  completed ${fullname}"
}

grid()
{
    length="$1"
    format="$2"

    scale="$3"

    fullname="${name}_${length}_${format}-gridded"
    folder="./output/${fullname}"
    echo "Processing grid for ${fullname}"

    resized="./temp/${source%%.*}-resized_for_${length}.${source##*.}"
    if [ ! -e "$resized" ]; then
        echo "  Error: Source resized image not present: ${resized}"
        exit 1
    fi
    new="./temp/${source%%.*}-resized_for_${length}-for_grid.${format}"
    
    width=$(identify -format '%w' "$resized")
    height=$(identify -format '%h' "$resized")

    if [ "$width" -gt "$height" ]; then
        max=$width
    else
        max=$height
    fi

    if [ -z "$scale" ]; then
        scale=$((max / 1472))
        if [ $scale -lt 4 ]; then
            scale=4
        fi
    fi

    new_width=$((  $width / $scale ))
    new_height=$(( $height / $scale ))

    echo "  Creating resized grid image scaled by ${scale}: ${width}x${height} -> ${new_width}x${new_height}"
    mkdir -p "$(dirname "$new")"
    
    if [ ! -e "$new" ]; then
        echo "  Creating intermediate resized image for gridding: ${new}"
        convert "$resized" -resize "x${new_height}" +repage "$new"
    fi

    gridwidth=$(( $length / $scale))
    gridded="${folder}.${format}"

    if [ ! -e "$gridded" ]; then
        imagemagick-fred-grid.sh -d "${gridwidth},${gridwidth}" -c red -s "${gridwidth}" -o 0.7 "$new" "${gridded}"
    fi
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
    #clean

    source="$1"
    name="$2"

    if [ ! -e "$source" ]; then
        echo "Source ${source} not found"
        return 1
    fi 
    echo "Processing ${source}, named ${name}"

    formats="${source##*.}"
    if [ "${source##*.}" == "tif" ]; then
        formats="jpg ${formats}"
    fi
    for format in $formats
    do    
        for length in 256 512
        do
            process $length $format
            if [ "$format" == "jpg" ]; then
                grid $length $format $scale
            fi
        done
    done
}

#source="ex_moorea.jpg"
#name="orthophotomosaic_moorea"
#source="orthophotomosaic_CoralReef_reprojected.tif"
#name="orthophotomosaic_curacao"

#scale=4
#scale=16

main orthophotomosaic_CoralReef_reprojected.tif orthophotomosaic_curacao 
main ex_moorea.jpg orthophotomosaic_moorea


