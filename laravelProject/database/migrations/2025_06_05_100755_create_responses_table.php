<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('responses', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('document_id');
            $table->text('provider')->nullable();
            $table->text('publication_date')->nullable();
            $table->text('submission_deadline')->nullable();
            $table->text('procedure_title')->nullable();
            $table->text('purpose')->nullable();
            $table->text('funding_reference')->nullable();
            $table->text('cup')->nullable();
            $table->text('intervention_title')->nullable();
            $table->text('description')->nullable();
            $table->text('fund')->nullable();
            $table->text('required_characteristics')->nullable();
            $table->text('timelines')->nullable();
            $table->text('maximum_budget')->nullable();
            $table->text('deadline')->nullable();
            $table->text('email_for_quote')->nullable();
            $table->text('issuer_name')->nullable();
            $table->text('payment_method')->nullable();
            $table->text('company_relevance')->nullable();
            $table->foreign('document_id')->references('id')->on('documents')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('responses');
    }
};
