<?php

namespace App\Http\Controllers;

use App\Models\Conversation;
use Illuminate\Http\Request;

class ConversationController extends Controller
{
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
            'active' => 'boolean',
        ]);

        $conversation = Conversation::create([
            'title'  => $data['title']  ?? 'Nuova conversazione',
            'active' => $data['active'] ?? true,
        ]);

        return response()->json($conversation, 201);
    }

    /** GET /api/conversations/{conversation} */
    public function show(Conversation $conversation)
    {
        return $conversation;
    }
}
