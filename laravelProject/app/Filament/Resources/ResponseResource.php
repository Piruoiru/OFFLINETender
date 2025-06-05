<?php

namespace App\Filament\Resources;

use App\Filament\Resources\ResponseResource\Pages;
use App\Filament\Resources\ResponseResource\RelationManagers;
use App\Models\Response;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\SoftDeletingScope;

class ResponseResource extends Resource
{
    protected static ?string $model = Response::class;

    protected static ?string $navigationIcon = 'heroicon-o-circle-stack';

    protected static ?string $navigationGroup = 'Data Management';
    
    protected static ?int $navigationSort = 4;

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                Forms\Components\TextInput::make('document_id')
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('provider')
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('publication_date')
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('submission_deadline')
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('procedure_title')
                    ->columnSpanFull(),
                Forms\Components\Textarea::make('purpose')
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('funding_reference')
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('cup')
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('intervention_title')
                    ->columnSpanFull(),
                Forms\Components\Textarea::make('description')
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('fund')
                    ->columnSpanFull(),
                Forms\Components\Textarea::make('required_characteristics')
                    ->columnSpanFull(),
                Forms\Components\Textarea::make('timelines')
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('maximum_budget')
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('deadline')
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('email_for_quote')
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('issuer_name')
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('payment_method')
                    ->columnSpanFull(),
                Forms\Components\Textarea::make('company_relevance')
                    ->columnSpanFull(),
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('id')->searchable(),
                Tables\Columns\TextColumn::make('document_id')->searchable(),
                Tables\Columns\TextColumn::make('provider')->searchable(),
                Tables\Columns\TextColumn::make('publication_date')->searchable(),
                Tables\Columns\TextColumn::make('submission_deadline')->searchable(),
                Tables\Columns\TextColumn::make('procedure_title')->searchable(),
                Tables\Columns\TextColumn::make('purpose')->searchable(),
                Tables\Columns\TextColumn::make('funding_reference')->searchable(),
                Tables\Columns\TextColumn::make('cup')->searchable(),
                Tables\Columns\TextColumn::make('intervention_title')->searchable(),
                Tables\Columns\TextColumn::make('description')->searchable(),
                Tables\Columns\TextColumn::make('fund')->searchable(),
                Tables\Columns\TextColumn::make('required_characteristics')->searchable(),
                Tables\Columns\TextColumn::make('timelines')->searchable(),
                Tables\Columns\TextColumn::make('maximum_budget')->searchable(),
                Tables\Columns\TextColumn::make('deadline')->searchable(),
                Tables\Columns\TextColumn::make('email_for_quote')->searchable(),
                Tables\Columns\TextColumn::make('issuer_name')->searchable(),
                Tables\Columns\TextColumn::make('payment_method')->searchable(),
                Tables\Columns\TextColumn::make('company_relevance')->searchable(),
            ])
            ->filters([
                //
            ])
            ->actions([
                Tables\Actions\DeleteAction::make(),
            ])
            ->bulkActions([
                Tables\Actions\BulkActionGroup::make([
                    Tables\Actions\DeleteBulkAction::make(),
                ]),
            ]);
    }

    public static function getRelations(): array
    {
        return [
            //
        ];
    }

    public static function getPages(): array
    {
        return [
            'index' => Pages\ListResponses::route('/'),
            'create' => Pages\CreateResponse::route('/create'),
            'edit' => Pages\EditResponse::route('/{record}/edit'),
        ];
    }
}
