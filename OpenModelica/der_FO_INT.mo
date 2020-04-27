model der_FO_INT
  Modelica.Blocks.Sources.Pulse pulse(amplitude = 3000, nperiod = 1, offset = 0, period = 5000, startTime = 10, width = 80) annotation(
    Placement(visible = true, transformation(origin = {-86, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.LimPID pid annotation(
    Placement(visible = true, transformation(origin = {-42, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.FirstOrder firstOrder annotation(
    Placement(visible = true, transformation(origin = {8, -2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(pid.u_s, pulse.y) annotation(
    Line(points = {{-54, 0}, {-74, 0}}, color = {0, 0, 127}));
  connect(firstOrder.u, pid.y) annotation(
    Line(points = {{-4, -2}, {-30, -2}, {-30, 0}, {-30, 0}}, color = {0, 0, 127}));
  connect(pid.u_m, firstOrder.y) annotation(
    Line(points = {{-42, -12}, {18, -12}, {18, -2}, {20, -2}}, color = {0, 0, 127}));

annotation(
    uses(Modelica(version = "3.2.3")));
end der_FO_INT;
