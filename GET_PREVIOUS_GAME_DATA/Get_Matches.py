
from UTILITIES.Riot_APIS import RiotApi
from UTILITIES.Utilities import Utilities


class Get_Match_Timeline:
    def get_match_timeline(self,match_id):
        api_client = RiotApi()
        match_timeline = api_client.get_match_timeline(match_id)
        return match_timeline
    
    def get_events(self, match_timeline):
        events = []
        for frame in match_timeline['info']['frames']:
            for event in frame['events']:
                events.append(event)
        return events

class Get_Kills_Deaths_Assists:
    def get_deaths(self, events, participant_id):
        deaths = []
        for event in events:
            if event['type'] == 'CHAMPION_KILL':
                if event['victimId'] == participant_id:
                    deaths.append("death")
        return deaths
    
    def get_kills(self, events, participant_id):
        kills_event = []
        deaths_event = []
        assist_event = []
        for event in events:
            if event['type'] == 'CHAMPION_KILL':
                if event['killerId'] == participant_id:   
                    kill = self.extract_kill_data(event,participant_id)
                    if kill is not None:
                        kills_event.append(kill) 
                elif event['victimId'] == participant_id:
                    death = self.extract_death_data(event,participant_id)
                    if death is not None:
                        deaths_event.append(death)
                elif 'assistingParticipantIds' in event and participant_id in event['assistingParticipantIds']:
                    assist = self.extract_assist_data(event, participant_id)
                    if assist is not None:
                        assist_event.append(assist)
        return kills_event, deaths_event, assist_event

    def extract_kill_data(self, event,participant_id):
        required_keys = ['position', 'timestamp', 'victimId']
        all_keys_except_assist = all(key in event for key in required_keys)
        has_assist = 'assistingParticipantIds' in event
        if all_keys_except_assist and has_assist:  # If both conditions are True
            
            kill = Kill(
                assisting_participant_ids=[aid - 1 for aid in event.get('assistingParticipantIds', [])],
                killer_id=participant_id,
                position=Utilities.format_position(event['position']),
                timestamp=Utilities.convert_timestamp_to_game_time(event['timestamp']),
                victim_id=event['victimId']
            )
            return kill
        elif not has_assist:
            kill = Kill(
                killer_id=participant_id,
                position=Utilities.format_position(event['position']),
                 timestamp=Utilities.convert_timestamp_to_game_time(event['timestamp']),
                victim_id=event['victimId']
            )
            return kill
        else:
            return None
        
    def extract_death_data(self, event,participant_id):
        required_keys = ['position', 'killerId', 'victimId']
        all_keys_except_assist = all(key in event for key in required_keys)
        has_assist = 'assistingParticipantIds' in event

        if all_keys_except_assist and has_assist:  # If both conditions are True
            
            kill = Kill(
                assisting_participant_ids=[aid - 1 for aid in event.get('assistingParticipantIds', [])],
                killer_id=event['killerId'],
                position=Utilities.format_position(event['position']),
                timestamp=Utilities.convert_timestamp_to_game_time(event['timestamp']),
                victim_id=participant_id
            )
            return kill
        elif not has_assist:
            kill = Kill(
                killer_id=event['killerId'],
                position=Utilities.format_position(event['position']),
                 timestamp=Utilities.convert_timestamp_to_game_time(event['timestamp']),
                victim_id=participant_id
            )
            return kill
        else:
            return None
            
    def extract_assist_data(self, event,participant_id):
        required_keys = ['position', 'killerId', 'victimId']
        all_keys_except_assist = all(key in event for key in required_keys)
        has_assist = 'assistingParticipantIds' in event

        if all_keys_except_assist and has_assist:  # If both conditions are True
            
            kill = Kill(
                assisting_participant_ids=[aid - 1 for aid in event.get('assistingParticipantIds', [])],
                killer_id=event['killerId'],
                position=Utilities.format_position(event['position']),
                timestamp=Utilities.convert_timestamp_to_game_time(event['timestamp']),
                victim_id=event['victimId']
            )
            return kill
        else:
            return None       
        
class Kill:
    def __init__(self, killer_id, position, timestamp, victim_id, assisting_participant_ids=0):
        self.killer_id = killer_id -1
        self.position = position
        self.timestamp = timestamp
        self.victim_id = victim_id - 1
        self.assisting_participant_ids = assisting_participant_ids
    
    def __str__(self):
        return (f"Assisting Ids: {self.assisting_participant_ids}, "
                f"killer_id: {self.killer_id}, "
                f"position: {self.position}, "
                f"timestamp: {self.timestamp}, "
                f"victim_id: {self.victim_id}")
    













        

        

    