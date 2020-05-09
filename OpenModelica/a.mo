model a
  Modelica.Blocks.Sources.Pulse pulse(amplitude = 80, nperiod = 1, offset = 22, period = 11000, startTime = 0, width = 50)  annotation(
    Placement(visible = true, transformation(origin = {-80, -6}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.LimPID pid annotation(
    Placement(visible = true, transformation(origin = {-38, -6}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.SecondOrder secondOrder(D = 1.43178, k = 0.024, w = 549.342, yd(start = 27))  annotation(
    Placement(visible = true, transformation(origin = {6, -6}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.FirstOrder firstOrder(T = 17.906, k = 1)  annotation(
    Placement(visible = true, transformation(origin = {-78, -66}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(secondOrder.u, pid.y) annotation(
    Line(points = {{-6, -6}, {-27, -6}}, color = {0, 0, 127}));
  connect(pid.u_s, pulse.y) annotation(
    Line(points = {{-50, -6}, {-68, -6}}, color = {0, 0, 127}));
  connect(firstOrder.u, secondOrder.y) annotation(
    Line(points = {{-90, -66}, {-90, -36}, {18, -36}, {18, -6}}, color = {0, 0, 127}));
  connect(pid.u_m, firstOrder.y) annotation(
    Line(points = {{-38, -18}, {-45.5, -18}, {-45.5, -66}, {-67, -66}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "3.2.3")));
end a;
