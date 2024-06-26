from lavalink import LoadType

from config import CLIENT


async def add_song_recommendations(bot_user, player, number, inputs, retries: int = 1):
    input_string = ""
    for song, artist in inputs.items():
        input_string += f"{song} - {artist}, "
    # Remove the final ", "
    input_string = input_string[:-2]

    completion = (
        CLIENT.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""I need songs that are similar in nature to ones that I list.
                            Send {number} songs formatted as:

                                SONG NAME - ARTIST NAME
                                SONG NAME - ARTIST NAME
                                ...

                            Do not provide anything except for the exactly what I need, no
                            list numbers, no quotations, only what I have shown.

                            The songs you should base the list off of are: {input_string}

                            NOTE: If you believe that there are not many songs that are similar to the ones I list, then please just respond with the message "SONG FIND ERROR"
                """,
                }
            ],
            model="gpt-3.5-turbo",
        )
        .choices[0]
        .message.content.strip()
        .strip('"')
    )

    # Sometimes, we get false failures, so we check for a failure, and it we haven't tried
    # at least 3 times, then continue retrying, otherwise, we actually can't get any songs
    if completion == "SONG FIND ERROR":
        if retries <= 3:
            await add_song_recommendations(
                bot_user, player, number, inputs, retries + 1
            )
        else:
            return False

    else:
        for entry in completion.split("\n"):
            song, artist = entry.split(" - ")

            ytsearch = f"ytsearch:{song} {artist} audio"
            results = await player.node.get_tracks(ytsearch)

            if not results.tracks or results.load_type in (
                LoadType.EMPTY,
                LoadType.ERROR,
            ):
                dzsearch = f"dzsearch:{song} {artist}"
                results = await player.node.get_tracks(dzsearch)

                if not results.tracks or results.load_type in (
                    LoadType.EMPTY,
                    LoadType.ERROR,
                ):
                    continue

            track = results.tracks[0]
            player.add(requester=bot_user, track=track)

        return True
