from lavalink import LoadType
import re


async def add_song_recommendations(
    openai_client, bot_user, player, number, inputs, retries: int = 1
):
    input_list = [f'"{song} by {artist}"' for song, artist in inputs.items()]

    completion = (
        openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        BACKGROUND: You're an AI music recommendation system with a knack for understanding
                        user preferences based on provided input. Your task is to generate a list
                        of {number} songs that the user might enjoy, derived from a given list of {number} songs.
                        The input will be in the format of
                            ["Song-1-Name by Song-1-Artist", "Song-2-Name by Song-2-Artist", ...]
                        and you need to return a list formatted in the same way.

                        When recommending songs, consider the genre, tempo, and mood of the input
                        songs to suggest similar ones that align with the user's tastes. Also, it
                        is important to mix up the artists, don't only give the same artists that
                        are already in the queue. If you cannot find {number} songs that match the
                        criteria or encounter any issues, return the list ["NOTHING FOUND"].

                        Please be sure to also only use characters A-Z, a-z, 0-9, and spaces in the
                        song and artist names. Do not include escape/special characters, emojis, or
                        quotes in the output.

                        INPUT: {input_list}
                    """,
                }
            ],
            model="gpt-4o-mini",
        )
        .choices[0]
        .message.content.strip()
        .strip('"')
    )

    # Sometimes ChatGPT will return `["NOTHING FOUND"]` even if it should
    # have found something, so we check each prompt up to 3 times before
    # giving up.
    if completion == '["NOTHING FOUND"]':
        if retries <= 3:
            await add_song_recommendations(
                openai_client, bot_user, player, number, inputs, retries + 1
            )
        else:
            return False

    else:
        # Clean up the completion string to remove any potential issues
        # with the eval function (e.g. OUTPUT: prefix, escaped quotes, etc.)
        completion = re.sub(r"[\\\'\[\]\n]+|OUTPUT: ", "", completion)

        for entry in eval(completion):
            song, artist = entry.split(" by ")
            ytsearch = f"ytsearch:{song} by {artist} audio"
            results = await player.node.get_tracks(ytsearch)

            if (
                not results
                or not results.tracks
                or not results.load_type
                or results.load_type
                in (
                    LoadType.EMPTY,
                    LoadType.ERROR,
                )
            ):
                dzsearch = f"dzsearch:{song}"
                results = await player.node.get_tracks(dzsearch)

                if (
                    not results
                    or not results.tracks
                    or not results.load_type
                    or results.load_type
                    in (
                        LoadType.EMPTY,
                        LoadType.ERROR,
                    )
                ):
                    continue

            track = results.tracks[0]
            player.add(requester=bot_user, track=track)

        return True
