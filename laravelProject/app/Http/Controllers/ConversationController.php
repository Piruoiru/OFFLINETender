<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Conversation;
use App\Models\Message;
use Illuminate\Http\Request;

class ConversationController extends Controller
{
    // Ritorna tutte le conversazioni
    public function conversations()
    {
        return response()->json(Conversation::all());
    }

    // Ritorna tutti i messaggi di una conversazione specifica
    public function messages($id)
    {
        $conversation = Conversation::findOrFail($id);
        $messages = $conversation->messages()->with('user')->get(); // Assumendo relazione messages() in Conversation

        return response()->json($messages);
    }

    // Salva un nuovo messaggio per una conversazione
    public function storeMessage(Request $request, $id)
    {
        $request->validate([
            'content' => 'required|string',
        ]);

        $message = Message::create([
            'conversation_id' => $id,
            'sender' => 'user',
            'content' => $request->content,
        ]);

        return response()->json($message, 201);
    }
}
