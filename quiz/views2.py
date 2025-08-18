from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Quiz, Question, QuizProgress
from .serializer2 import QuizDetailSerializer, QuestionSerializer

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_quiz_with_progress(request, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    # Get or create the QuizProgress for this user and quiz
    progress, created = QuizProgress.objects.get_or_create(user=user, quiz=quiz)
    
    # Serialize the full quiz object
    quiz_serializer = QuizDetailSerializer(quiz)

    # Filter out questions that have already been answered
    answered_ids = progress.answered_questions
    remaining_questions_queryset = quiz.questions.exclude(id__in=answered_ids)
    remaining_questions_serializer = QuestionSerializer(remaining_questions_queryset, many=True)
    
    quiz_is_complete = not remaining_questions_queryset.exists()

    response_data = {
        "quiz_info": quiz_serializer.data,
        "remaining_questions": remaining_questions_serializer.data,
        "quiz_is_complete": quiz_is_complete,
        "progress": {
            "current_question_index": progress.current_question_index,
            "answered_count": len(answered_ids),
            "total_questions": quiz.questions.count()
        }
    }
    print(response_data, 'response_data')
    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_answer_and_progress(request, quiz_id):
    """
    Saves a user's answer and updates their progress record in the database.
    """
    user = request.user
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    # Get the data from the request
    answered_question_id = request.data.get('question_id')
    chosen_option_id = request.data.get('choice_id')
    print(answered_question_id,chosen_option_id)
    
    if not answered_question_id or not chosen_option_id:
        return Response(
            {"error": "question_id and choice_id are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get or create the QuizProgress for this user and quiz
    progress, created = QuizProgress.objects.get_or_create(user=user, quiz=quiz)

    # Check if this question has already been answered
    print(progress.answered_questions, 'progress.answered_questions')
    if answered_question_id in progress.answered_questions:
        return Response(
            {"message": "Question has already been answered."},
            status=status.HTTP_409_CONFLICT
        )
    
    # Append the new question to the answered list
    progress.answered_questions.append(answered_question_id)
    
    # Find the index of the next question
    # This logic assumes questions are ordered by creation date or ID
    all_questions = quiz.questions.order_by('id').values_list('id', flat=True)
    try:
        current_index = list(all_questions).index(answered_question_id)
        progress.current_question_index = current_index + 1
    except ValueError:
        # The answered question ID was not found in the quiz's questions
        # This shouldn't happen, but we handle it gracefully
        pass

    # Save the updated progress
    progress.save()

    return Response(
        {"message": "Answer saved and progress updated successfully."},
        status=status.HTTP_200_OK
    )
