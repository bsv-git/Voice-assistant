from contextlib import contextmanager
from unittest import TestCase
from unittest.mock import patch

import main


@contextmanager
def _tracked_session(tracker):
    tracker["entered"] += 1
    try:
        yield
    finally:
        tracker["exited"] += 1


class RunAssistantTests(TestCase):
    def test_tool_route_handles_time_without_model_call(self):
        with patch("main.start_realtime_session", return_value=_tracked_session({"entered": 0, "exited": 0})), patch(
            "main.transcribe_audio", side_effect=["what time is it", "exit"]
        ), patch("main.generate_response") as generate_response, patch("main.speak") as speak, patch(
            "main.save_interaction"
        ) as save_interaction:
            main.run_assistant()

        generate_response.assert_not_called()
        speak.assert_called_once()
        save_interaction.assert_called_once()
        saved_response = save_interaction.call_args[0][1]
        self.assertTrue(saved_response.startswith("Current time: "))

    def test_realtime_session_persists_across_turns(self):
        tracker = {"entered": 0, "exited": 0}

        with patch("main.start_realtime_session", return_value=_tracked_session(tracker)), patch(
            "main.transcribe_audio", side_effect=["hello", "how are you", "exit"]
        ), patch("main.generate_response", side_effect=["one", "two"]) as generate_response, patch(
            "main.speak"
        ) as speak, patch("main.save_interaction") as save_interaction:
            main.run_assistant()

        self.assertEqual(tracker["entered"], 1)
        self.assertEqual(tracker["exited"], 1)
        self.assertEqual(generate_response.call_count, 2)
        self.assertEqual(speak.call_count, 2)
        self.assertEqual(save_interaction.call_count, 2)

    def test_max_turns_limits_processing(self):
        tracker = {"entered": 0, "exited": 0}

        with patch("main.start_realtime_session", return_value=_tracked_session(tracker)), patch(
            "main.transcribe_audio", side_effect=["hello", "again", "more"]
        ), patch("main.generate_response", side_effect=["one", "two", "three"]) as generate_response, patch(
            "main.speak"
        ) as speak, patch("main.save_interaction") as save_interaction:
            main.run_assistant(max_turns=2)

        self.assertEqual(tracker["entered"], 1)
        self.assertEqual(tracker["exited"], 1)
        self.assertEqual(generate_response.call_count, 2)
        self.assertEqual(speak.call_count, 2)
        self.assertEqual(save_interaction.call_count, 2)
