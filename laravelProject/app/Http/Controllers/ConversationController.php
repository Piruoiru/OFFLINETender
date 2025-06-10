<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Conversation;
use App\Models\Message;
use Illuminate\Http\Request;
use Symfony\Component\Process\Process;
use Illuminate\Support\Facades\Http;

class ConversationController extends Controller
{
    // Ritorna tutte le conversazioni
    public function conversations()
    {
        $conversations = Conversation::select('id', 'title', 'active', 'created_at')->get();
        return response()->json($conversations);
    }

    // Crea una nuova conversazione
    public function createConversation(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'active' => 'nullable|boolean',
        ]);

        try {
            $conversation = Conversation::create([
                'title' => $validated['title'],
                'active' => $validated['active'] ?? true, // Usa true se non viene fornito
            ]);

            return response()->json([
                'success' => true,
                'conversation' => $conversation
            ], 201);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'error' => 'Errore nella creazione della conversazione.',
                'details' => $e->getMessage(),
            ], 500);
        }
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

    public function chat(Request $request)
    {
        $request->validate([
            'message' => 'required|string',
            'conversation_id' => 'required|integer',
        ]);

        try {
            $response = Http::timeout(300)->post('http://127.0.0.1:5050/chat', [
                'message' => $request->input('message'),
                'conversation_id' => $request->input('conversation_id'),
            ]);

            if ($response->failed()) {
                return response()->json([
                    'error' => 'Errore dal backend Python',
                    'details' => $response->json(),
                ], 500);
            }

            return response()->json($response->json());

        } catch (\Exception $e) {
            return response()->json([
                'error' => 'Errore nella comunicazione con il backend Python',
                'details' => $e->getMessage(),
            ], 500);
        }
    }

}
