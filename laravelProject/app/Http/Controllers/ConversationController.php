<?php

namespace App\Http\Controllers;

use App\Models\Conversation;
use Illuminate\Http\Request;
use App\Repositories\Contracts\ConversationRepositoryInterface;

class ConversationController extends Controller
{
    protected ConversationRepositoryInterface $conversationRepository;
    
       public function __construct(
            ConversationRepositoryInterface $conversationRepository
       )
       {   
           $this->conversationRepository = $conversationRepository;
       }

    /** GET /api/conversations */
    public function index()
    {
        return Conversation::oldest()->get();
    }

    /** POST /api/conversations */
    public function storeConversation(Request $request)
    {
        $data = $request->validate([
            'title'  => 'nullable|string|max:255',
        ]);

        $conversation= $this->conversationRepository->store([
            'title'  => $data['title'] ?? 'Nuova conversazione',
            'user_id' => auth()->id(),
        ]);

        return response()->json($conversation, 201);
    }

    /** GET /api/conversations/{conversation} */
    public function show(Conversation $conversation)
    {
        return $conversation;
    }
}
