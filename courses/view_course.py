from fastapi import APIRouter, HTTPException, Depends
from middleware.token_verification import check_token

router = APIRouter()

@router.get("/courses-detail/{course_id}", dependencies=[Depends(check_token)])
async def get_course_details(course_id: str):
    # Static data (same as what you provided)
    course_details = {
        "id": "68c4057a84f9715dbc9dd470",
        "title": "AI & Deep Learning Masterclass",
        "description": "A complete introduction to neural networks, deep learning concepts, and hands-on AI projects.",
        "image_url": "https://th.bing.com/th/id/OIP.fd2oR5ZtGVqq6YoLhcgYHQHaEc",
        "intro_video": "https://1500042575.vod-qcloud.com/145298b5vodsgp1500042575/22e8a0e55145403704472682459/4szxD0G6Ag4A.mp4",
        "rating": 4.7,
        "reviews": "(280 Reviews)",
        "total_lecture": "24 Lectures",

        "instructor": {
            "id": "instructor_102",
            "photo": "https://cdn.pixabay.com/photo/2024/09/12/21/20/ai-generated-9043367_1280.png",
            "name": "Dr. Arjun Mehta",
            "designation": "AI Research Scientist"
        },

        "skills": [
            {"name": "Neural Networks"},
            {"name": "Deep Learning"},
            {"name": "TensorFlow"},
            {"name": "Machine Learning"}
        ],

        "lectures": [
            {
                "id": 1,
                "type": "video",
                "videos": {
                    "title": "Introduction to Deep Learning",
                    "name": "intro_deep_learning",
                    "duration": "5 min",
                    "is_watched": True,
                    "progress_percentage": 100,
                    "url": "https://1500042575.vod-qcloud.com/145298b5vodsgp1500042575/cea707575145403704471343119/TLq3WAn73goA.mp4"
                }
            },
            {
                "id": 2,
                "type": "video",
                "videos": {
                    "title": "Neural Networks Basics",
                    "name": "nn_basics",
                    "duration": "8 min",
                    "is_watched": True,
                    "progress_percentage": 76,
                    "url": "https://1500042575.vod-qcloud.com/145298b5vodsgp1500042575/68e405245145403704473383936/erEkYN0vFZUA.mp4"
                }
            },
            {
                "id": 3,
                "type": "test",
                "mock_test": [
                    {
                        "question_id": 1,
                        "question": "Which activation function is commonly used?",
                        "options": ["ReLU", "Dropout", "Batch Norm", "Pooling"]
                    },
                    {
                        "question_id": 2,
                        "question": "Which algorithm trains neural networks?",
                        "options": ["Back propagation", "Divide & Conquer", "Greedy Search", "K-Means"]
                    }
                ]
            },
            {
                "id": 4,
                "type": "video",
                "videos": {
                    "title": "Convolutional Neural Networks",
                    "name": "cnn_intro",
                    "duration": "12 min",
                    "is_watched": False,
                    "progress_percentage": 0,
                    "url": "https://1500042575.vod-qcloud.com/145298b5vodsgp1500042575/22e8a0e55145403704472682459/4szxD0G6Ag4A.mp4"
                }
            },
            {
                "id": 5,
                "type": "test",
                "mock_test": [
                    {
                        "question_id": 3,
                        "question": "Which layer is used for reducing spatial dimensions?",
                        "options": ["Pooling Layer", "Dense Layer", "Softmax Layer", "Embedding Layer"]
                    }
                ]
            }
        ]
    }

    return {
        "status": "Success",
        "message": "Course details",
        "data": course_details
    }
