from lipsgit.models import Emoji


def semantic_commit_matching(
    commit_title: str, available_emojis: list[Emoji]
) -> list[Emoji]:
    from sentence_transformers import SentenceTransformer, util

    # Load a pre-trained model for sentence embeddings
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

    description_emoji_map = {
        emoji.description: emoji for emoji in available_emojis
    }
    emoji_descriptions = [emoji.description for emoji in available_emojis]

    commit_message_embedding = model.encode(
        commit_title.lower(), convert_to_tensor=True
    )
    emoji_embeddings = model.encode(emoji_descriptions, convert_to_tensor=True)

    similarity_scores = util.cos_sim(
        commit_message_embedding, emoji_embeddings
    )[0].tolist()

    sorted_emoji_descriptions = [
        emoji
        for emoji, _ in sorted(
            zip(emoji_descriptions, similarity_scores),
            key=lambda x: x[1],
            reverse=True,
        )
    ]

    return [
        description_emoji_map[emoji_description]
        for emoji_description in sorted_emoji_descriptions
    ]
